#!/bin/bash
# cd /usr/share/nginx/html
# rm -r dist
# cd /home/ec2-user/src
# sed -i 's,ws://localhost:5000,wss://playopulence.com,1' websocket.js
# cd /home/ec2-user
# npm run build
# mv dist /usr/share/nginx/html
cd /home/ubuntu
source .venv/bin/activate
pip3 install -r requirements.txt