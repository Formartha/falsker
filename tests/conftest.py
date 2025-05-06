import os
import subprocess
import time
import pytest
import logging
from flasker_sdk.client import FlaskerClient

API_TOKEN = "admin123"
HOST = "127.0.0.1"
PORT = "5003"

project_root = os.path.join(os.path.dirname(os.path.dirname(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def start_stack():
    env = os.environ.copy()
    env["API_TOKEN"] = API_TOKEN
    compose_loc = os.path.join(project_root, "flasker", "docker-compose.yml")

    logger.info("Starting Flasker stack using Docker Compose...")
    try:
        subprocess.run(
            ["docker-compose", "-f", compose_loc, "up", "--build", "flasker", "-d"],
            env=env,
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.error("Docker Compose failed to start the stack.")
        raise RuntimeError("Docker Compose failed to start the stack.") from e

    logger.info("Waiting for Flasker service to be ready...")
    wait_for_flasker_sdk_ready(token=API_TOKEN)
    logger.info("Flasker stack is ready.")

    yield

    logger.info("Stopping Flasker stack...")
    subprocess.run(["docker-compose", "-f", compose_loc, "down"], check=True)
    logger.info("Flasker stack stopped.")


def wait_for_flasker_sdk_ready(token, timeout=30):
    client = FlaskerClient(host=HOST, port=PORT, token=token)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            data = client.health()
            if data.get("status") in ["OK", "DEGRADED"]:
                return
        except Exception:
            logger.debug("Waiting for service...")
        time.sleep(1)
    raise TimeoutError("Flasker stack did not become ready in time.")


@pytest.fixture(scope="module")
def client():
    return FlaskerClient(host=HOST, port=PORT, token=API_TOKEN)
