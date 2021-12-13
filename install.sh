#!/bin/bash
apt install python3-dev

echo 'Creating service...'
cp -u -r service/wb-deltaups.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable wb-deltaups.service

cp -u -r source /mnt/data/etc/wb-deltaups && cd /mnt/data/etc/wb-deltaups || exit

echo 'Installing venv...'
python3 -m venv venv
source venv/bin/activate

echo 'Installing requirements...'
pip install -r requirements.txt
deactivate

echo 'Starting service...'
systemctl start wb-deltaups.service