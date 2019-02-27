#!/bin/bash
sudo adduser --system --no-create-home --group node_exporter

sudo cp ./files/node_exporter.service   /etc/systemd/system/node_exporter.service
sudo mkdir /etc/node_exporter
sudo cp ./files/sysconfig.node_exporter /etc/node_exporter/node_exporter

sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

sudo cp ./files/zero-appliance.service   /etc/systemd/system/zero-appliance.service

sudo systemctl daemon-reload
sudo systemctl enable zero-appliance
sudo systemctl start zero-appliance

#sudo cp ./files/zero-exporter.service   /etc/systemd/system/zero-exporter.service

#sudo systemctl daemon-reload
#sudo systemctl enable zero-exporter
#sudo systemctl start zero-exporter
