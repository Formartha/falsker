import os
from flask import Flask, request, jsonify
from endpoints import bp


def create_app():
    app = Flask(__name__)
    app.config["API_TOKEN"] = os.environ.get("API_TOKEN", "admin123")  # if no secret was provided during creation, use admin123

    @app.before_request
    def check_token():
        token = request.headers.get("X-Token")
        if token != app.config["API_TOKEN"]:
            return jsonify({"error": "Unauthorized"}), 401

    app.register_blueprint(bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5003)
