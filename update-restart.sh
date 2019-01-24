#!/bin/bash
git pull origin master

echo 'Restarting zero-appliance'
sudo systemctl restart zero-appliance

echo 'Restarting zero-exporter'
sudo systemctl restart zero-exporter

echo 'Done'
