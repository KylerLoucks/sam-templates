#!/bin/bash
systemctl stop nginx
killall gunicorn > /dev/null 2>&1