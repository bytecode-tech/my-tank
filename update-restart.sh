#!/bin/bash
git pull origin

echo 'Restarting zero-appliance'
sudo systemctl restart zero-appliance

echo 'Restarting zero-exporter'
sudo systemctl restart zero-exporter

echo 'Done'
