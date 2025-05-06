import psutil
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from db_connector import get_redis_connection
from schemas import UserSchema

bp = Blueprint("api", __name__)
r = get_redis_connection()
user_schema = UserSchema()


@bp.route("/health", methods=["GET"])
def health_check():
    try:
        redis_status = r.ping()
    except Exception:
        redis_status = False

    cpu_percent = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    mb = 1024 ** 2  # bytes to megabytes

    return jsonify({
        "status": "OK" if redis_status else "DEGRADED",
        "db_connected": redis_status,
        "system": {
            "cpu_percent": cpu_percent,
            "memory": {
                "total_mb": round(mem.total / mb, 2),
                "available_mb": round(mem.available / mb, 2),
                "used_mb": round(mem.used / mb, 2),
                "percent": mem.percent
            },
            "disk": {
                "total_mb": round(disk.total / mb, 2),
                "used_mb": round(disk.used / mb, 2),
                "free_mb": round(disk.free / mb, 2),
                "percent": disk.percent
            }
        }
    }), 200 if redis_status else 503


@bp.route("/users", methods=["GET"])
def list_users():
    return jsonify({"users": r.keys()}), 200


@bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user_id = data["id"]

    if r.exists(user_id):  # Redis expects string key
        return jsonify({"error": "User already exists"}), 409

    r.hset(user_id, mapping=data)
    return jsonify({"message": "User created"}), 201


@bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if not r.exists(user_id):
        return jsonify({"error": "User not found"}), 404
    return jsonify(r.hgetall(user_id)), 200
