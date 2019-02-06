#!/bin/bash

sudo easy_install pip
sudo pip install setuptools

sudo apt-get install git-core
#GEN SSH Keys before git


git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT

sudo apt-get install build-essential python-dev

sudo python setup.py install

cd ~
cd zero-appliance
sudo pip install -r requirements.txt
cd ~

pip install prometheus_client


# Install and run node exporter for pi stats
curl -SL https://github.com/prometheus/node_exporter/releases/download/v0.16.0/node_exporter-0.16.0.linux-armv6.tar.gz > node_exporter.tar.gz && \
sudo tar -xvf node_exporter.tar.gz -C /usr/local/bin/ --strip-components=1

node_exporter &

# Install docker
#curl -sSL https://get.docker.com | sh 
#Depricated, now use apt with older ver
sudo apt-get install docker-ce=18.06.1~ce~3-0~raspbian

# run prometheus docker image
docker run -dit --restart unless-stopped --net=host -p 9090:9090 -v /home/pi/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml -v prometheus-data:/var/lib/prometheus/ faucet/prometheus-pi

git clone git@github.com:bytecode-tech/zero-appliance.git

git clone git@github.com:bytecode-tech/aspen-app.git
