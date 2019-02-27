#!/bin/bash

sudo systemctl stop zero-exporter
sudo rm -rf /etc/systemd/system/zero-exporter.service 

docker run -dit --restart unless-stopped --net=host -p 9090:9090 --name weegrow_prometheus -v /home/pi/zero-appliance/prometheus.yml:/etc/prometheus/prometheus.yml -v prometheus-data:/var/lib/prometheus/ faucet/prometheus-pi
docker run --net=host -d -p 80:80 --restart unless-stopped --name weegrow_app joshdmoore/aspen-app:latest