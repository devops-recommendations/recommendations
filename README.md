# Recommendations service.

### Overview

This is the repository that houses the recommendations service that is part of the NYU class **CSCI-GA.2810-001: DevOps
and Agile Methodologies**

## Setup

1. Clone the repo.
2. Start your Docker Daemon / Virtualbox.
3. From the project root,
    - if you're on an M1 mac, execute `vagrant up --provider docker`
    - if you're on a Windows PC, execute `vagrant up --provider virtualbox`
4. After this, you will find a vm / docker container running on your system, inside which a docker container running
   postgres.
5. To start the flask app, run `./scripts/start.sh` from the project directory. This will start the flask app on
   port `5000`.

- Server logs will be output in the same terminal window.
- You can test the service by executing `curl 127.0.0.1/5000` from your shell/terminal.

## Structure

```text
.gitignore                  - this will ignore vagrant and other metadata files
requirements.txt            - list if Python libraries required by your code
config.py                   - configuration parameters

service/                    - service python package
├── __init__.py             - package initializer
├── error_handlers.py       - HTTP error handling code
├── models.py               - module with business models
├── routes.py               - module with service routes
└── status.py               - HTTP status constants

tests/                      - test cases package
├── __init__.py             - package initializer
├── test_models.py          - test suite for busines models
├── test_db_connection.py   - test suite for db connections
├── factories.py            - test factory to instantiate objects for testing
└── test_routes.py          - test suite for service routes

Vagrantfile                 - sample Vagrant file that installs Python 3 and PostgreSQL
```
