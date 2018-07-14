#!/bin/bash

# Install and run node exporter for pi stats
curl -SL https://github.com/prometheus/node_exporter/releases/download/v0.14.0/node_exporter-0.14.0.linux-armv6.tar.gz > node_exporter.tar.gz && \
sudo tar -xvf node_exporter.tar.gz -C /usr/local/bin/ --strip-components=1

node_exporter &

# Install docker
curl -sSL https://get.docker.com | sh

# run prometheus docker image
docker run -dit --restart unless-stopped --net=host -p 9090:9090 -v /home/pi/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml -v prometheus-data:/var/lib/prometheus/ faucet/prometheus-pi