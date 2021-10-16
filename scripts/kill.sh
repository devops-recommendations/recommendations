# Kill the flask app running within the VM.

vagrant ssh -c 'sudo kill -9 $(sudo lsof -t -i:5000)'