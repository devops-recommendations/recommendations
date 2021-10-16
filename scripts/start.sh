# Starts the flask app running within the VM.

vagrant ssh -c '. ~/venv/bin/activate && cd /vagrant && FLASK_APP=service:app flask run -h 0.0.0.0'