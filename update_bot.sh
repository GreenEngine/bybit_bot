#!/bin/bash

cd /root/bybit_bot
sudo systemctl stop bibi.service
git pull
pip install -r requirements.txt
sudo systemctl start bibi.service