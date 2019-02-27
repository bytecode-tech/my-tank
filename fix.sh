#!/bin/bash

sudo systemctl stop zero-exporter
sudo rm -rf /etc/systemd/system/zero-exporter.service 

sudo apt-get install libpcre3 libpcre3-dev -y

sudo pip3 install uwsgi -I --no-cache-dir

sudo docker pull joshdmoore/aspen-app

sudo ./scripts/node_exporter_service.sh

sudo docker run -dit --restart unless-stopped --net=host -p 9090:9090 --name weegrow_prometheus -v /home/pi/zero-appliance/prometheus.yml:/etc/prometheus/prometheus.yml -v prometheus-data:/var/lib/prometheus/ faucet/prometheus-pi
sudo docker run --net=host -d -p 80:80 --restart unless-stopped --name weegrow_app joshdmoore/aspen-app:latest