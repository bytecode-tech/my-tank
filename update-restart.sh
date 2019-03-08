#!/bin/bash
git pull origin

#install pip requirements
sudo pip3 install -r requirements.txt

echo 'Restarting zero-appliance'
sudo systemctl restart zero-appliance

echo 'Done'
