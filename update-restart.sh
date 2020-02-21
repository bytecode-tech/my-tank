#!/bin/bash
git pull origin

#install pip requirements
sudo pip3 install -r requirements.txt

echo 'Restarting observer-appliance'
sudo systemctl restart observer-appliance

echo 'Done'
