# Recommendations service.

## Setup

- Clone the repo.
- From the project root,
    - if you're on an M1 mac, execute `vagrant up --provider docker`
    - if you're on a Windows PC, execute `vagrant up --provider virtualbox`
- This will bring up a vm / docker container.
    - Within this vm / container, you will find
        - a docker container running a `postgres` instance.
        - an instance of the flask app running on port 5000.
- Test the service by executing `curl 127.0.0.1/5000` from your shell/terminal.
