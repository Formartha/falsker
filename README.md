What?
-----
Flasker is a lightweight RESTful web application built with Flask, Redis, and Docker.
Flasker is designed to manage user data and expose basic system health metrics.
The application validates Israeli ID numbers, enforces API token authentication, and is packaged for local development and testing via Docker Compose.

Architecture
------------
The project is built from three main packages:
1. flasker - the ID store system
2. flasker_sdk - an installable pkg that allows interacting with flasker
3. tests - directory that stores the end to end tests of the client and the system

APIs
----
``` 
- `POST /users` — Create a new user
- `GET /users/<id>` — Retrieve user details by ID
- `GET /users` — List all user IDs
``` 

Security
---------
All endpoints require an `X-Token` header
Token is configurable via environment variable (`API_TOKEN`)
Note: default is set to `admin123`


How to deploy?
-----------
1. Install docker-compose and docker
2. run: ```docker-compose up --build flasker``` in flasker directory (ensure docker-compose.yaml is there)
3. access the ui via http://127.0.0.1:5002

Example:
--------
``` 
POST /users
{
  "id": "231740705",
  "phone": "+972501234567",
  "name": "Alice Tester",
  "address": "123 Test St, Tel Aviv"
}
```

Installation:
------------
The client could be either built from source with using `pip install -e full\path\to\flasker_sdk`.
Upon installation the flasker_sdk will be avilable for usage as standard python library.

Future:
-------
As this project is modular, the following items are coming soon:
1. Provide more APIs to manage the data and delete it
2. Dynamic database selection (create DAO properly to secure ability to multiple vendors)
3. Frontend to display and manage the data
4. Store the client in PyPi repository as well as full CI with triggering the tests to validate it
5. dynamic API building using JSON schema parser