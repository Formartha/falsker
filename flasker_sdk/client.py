import requests
import logging

logger = logging.getLogger()


class FlaskerClient:
    """
    Client used to connect to Flasker application
    """
    def __init__(self, host, port, token):
        """
        :param host: str # flasker host ip
        :param port: str # flasker port number
        :param token: str # required for connecting the flasker app
        """
        self.base_url = f"http://{host}:{port}"
        self.headers = {"X-Token": token}
        logger.info(f"Initialized FlaskerClient at {self.base_url}")

    def health(self):
        """ checks that the flasker app is working and running correctly """
        url = f"{self.base_url}/health"
        logger.info("Checking server health")
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            logger.info(f"Health check OK [{resp.status_code}]: {resp.json()}")
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: {e}")
            raise

    def list_users(self):
        """ returns list of users registered in the flasker database """
        url = f"{self.base_url}/users"
        logger.info("Listing users")
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            logger.info(f"Users listed [{resp.status_code}]: {resp.json()}")
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list users: {e}")
            raise

    def get_user(self, user_id):
        """ returns information about a registered user in flasker app, requires user id
        :param user_id: str
        """
        url = f"{self.base_url}/users/{user_id}"
        logger.info(f"Retrieving user with ID {user_id}")
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            logger.info(f"User retrieved [{resp.status_code}]: {resp.json()}")
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            raise

    def create_user(self, user_data):
        """ creates a user in flasker app, the payload data is a dict object with the following parameters:
        {
           "address": str, # free text
           "id": int,       # 9 digits
           "name": str,     # free text
           "phone": str     # should start with country prefix (e.g. +123xxx..)
        }
        """
        url = f"{self.base_url}/users"
        user_id = user_data.get("id")
        logger.info(f"Creating user with ID {user_id}")
        try:
            resp = requests.post(url, json=user_data, headers=self.headers)
            resp.raise_for_status()
            logger.info(f"User created [{resp.status_code}]: {resp.json()}")
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create user {user_id}: {e}")
            raise


if __name__ == "__main__":
    f = FlaskerClient("127.0.0.1", "5003", "admin123")
    f.list_users()
