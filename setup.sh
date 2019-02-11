#!/bin/bash

sudo apt-get install python3-pip python3-gpiozero -y
sudo python3 -m pip install --upgrade pip setuptools wheel

sudo apt-get install git-core -y
#GEN SSH Keys before git

cd zero-appliance
sudo pip3 install -r requirements.txt
cd ~

# Install and run node exporter for pi stats
curl -SL https://github.com/prometheus/node_exporter/releases/download/v0.16.0/node_exporter-0.16.0.linux-armv6.tar.gz > node_exporter.tar.gz && \
sudo tar -xvf node_exporter.tar.gz -C /usr/local/bin/ --strip-components=1

node_exporter &

# Install docker
#curl -sSL https://get.docker.com | sh 
#Depricated, now use apt with older ver
sudo apt-get install docker-ce=18.06.1~ce~3-0~raspbian

# run prometheus docker image
docker run -dit --restart unless-stopped --net=host -p 9090:9090 -v /home/pi/zero-appliance/prometheus.yml:/etc/prometheus/prometheus.yml -v prometheus-data:/var/lib/prometheus/ faucet/prometheus-pi

sudo  docker run --net=host -d -p 80:80 --restart unless-stopped joshdmoore/aspen-app:latest
