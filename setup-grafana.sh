wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.2.1_armhf.deb 
sudo apt-get install -y adduser libfontconfig
sudo apt --fix-broken install
sudo dpkg -i grafana_5.2.1_armhf.deb