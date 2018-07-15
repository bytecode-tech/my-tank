#!/bin/bash
sudo adduser --system --no-create-home --group node_exporter

sudo cp ./files/node_exporter.service   /etc/systemd/system/node_exporter.service
sudp cp ./files/sysconfig.node_exporter /etc/sysconfig/node_exporter

sudo systemctl reload-daemon
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

sudo cp ./files/zero-appliance.service   /etc/systemd/system/zero-appliance.service

sudo systemctl reload-daemon
sudo systemctl enable zero-appliance
sudo systemctl start zero-appliance

sudo cp ./files/zero-exporter.service   /etc/systemd/system/zero-exporter.service

sudo systemctl reload-daemon
sudo systemctl enable zero-exporter
sudo systemctl start zero-exporter
