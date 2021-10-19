# Recommendations service.

## Setup

- Clone the repo.
- Start the Docker Daemon / Virtualbox. 
- From the project root,
    - if you're on an M1 mac, execute `vagrant up --provider docker`
    - if you're on a Windows PC, execute `vagrant up --provider virtualbox`
- After this, you will find a vm / docker container running on your system, inside which a docker container running postgres. 
- To start the flask app, run `./scripts/start.sh` from the project directory. This will start the flask app on port `5000`.
  - Server logs will be output in the same terminal window.  
- You can check that the service is up and running by executing `curl -X GET http://localhost:5000` from your local shell/terminal. 
