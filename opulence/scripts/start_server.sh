#!/bin/bash
# cd /home/ec2-user
# systemctl start nginx
# runuser -l ec2-user -c 'screen -dmS "backend" python3.9 main.py'
cd /home/ubuntu
systemctl start nginx
source .venv/bin/activate
export PYTHON_ENV=prod
gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 wsgi:app -b 0.0.0.0:8000 --access-logfile gunicorn-access.log --error-logfile gunicorn-error.log --daemon