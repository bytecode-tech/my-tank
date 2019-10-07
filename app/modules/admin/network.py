from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
import os.path
import os
import threading
import logging
import time

class WifiNetwork():
    def __init__(self, *args, **kwargs):
        self.bssid = None
        self.ssid = None
        self.channel = None
        self.frequency = None
        self.mode = None
        self.type = None
        self.privacy = None
        self.signal_dbm = None
        self.signal_quality = None


        if 'bss' in kwargs:
            bss = kwargs.get('bss')

            self.bssid = bss.get_bssid()
            self.ssid = bss.get_ssid()
            self.channel = bss.get_channel()
            self.frequency = bss.get_frequency()
            self.mode = bss.get_mode()
            self.type = bss.get_network_type()
            self.privacy = bss.get_privacy()
            self.signal_dbm = bss.get_signal_dbm()
            self.signal_quality = bss.get_signal_quality()
            
class Network():
    def __init__(self, *args, **kwargs):
        self.ssid = None
        self.password = None
        self.enabled = False
        self.priority = None
        self.path = None

        if 'network' in kwargs:
            network = kwargs.get('network')

            self.enabled = network.get_enabled()
            self.path = network.get_path()
            properties = network.get_properties()
            self.ssid = properties.get('ssid')
            self.priority = properties.get('priority', '')

class Wifi():
    _LOGGER = logging.getLogger(__name__)

    def __init__(self):
        self._reactor = SelectReactor()
        threading.Thread(target=self._reactor.run, kwargs={'installSignalHandlers': 0}).start()
        time.sleep(0.1)  # let reactor start
        driver = WpaSupplicantDriver(self._reactor)
        supplicant = driver.connect()
        self.interface = supplicant.get_interface('wlan0')

    def __del__(self): 
        self._reactor.stop()

    def scan(self):
        scan_results = self.interface.scan(block=True)
        networks = []

        for bss in scan_results:
            networks.append(WifiNetwork(bss=bss))

        return networks

    def get_known_networks(self):
        results = self.interface.get_networks()
        networks = []
        for network in results:
            networks.append(Network(network=network))

        return networks


    def save_network(self, ssid: str, psk: str, enabled: bool, priority: str):
        network_config = { }

        #network_config['psk'] = psk
        network_config['ssid'] = ssid
        network_config['key_mgmt'] = "WPA-PSK"
        if enabled:
            network_config['enabled'] = 1

        network = self.interface.add_network(network_config)

        #Work around for psk invalid message format error
        #txdbus.error.RemoteError: org.freedesktop.DBus.Error.InvalidArgs: invalid message format
        network_id = os.path.basename(network.get_path())
        self._LOGGER.info("Saving network....Network path:" + network.get_path() + " Network Id: " + network_id)
        cmd = "wpa_cli -i wlan0 set_network " + network_id + " psk " + psk
        os.system(cmd)

        return Network(network=network)

    def get_network_info(self, name:str):
        results = self.interface.get_networks()

        found_network = None
        for network in results:
            ssid = network.get_properties().get('ssid')
            if ssid.lower() == name.lower():
                found_network = Network(network=network)
        
        return found_network

    def delete_network(self, name:str):
        results = self.interface.get_networks()

        for network in results:
            ssid = network.get_properties().get('ssid')
            if ssid.lower() == name.lower():
                self.interface.remove_network(network.get_path())
                break
    
    def activate_network(self, name:str):
        results = self.interface.get_networks()

        for network in results:
            ssid = network.get_properties().get('ssid')
            if ssid.lower() == name.lower():
                self.interface.select_network(network.get_path())
                break

    def get_active_network(self):
        network = self.interface.get_current_network()
        return Network(network=network)
    
    def save_config(self):
        cmd = "wpa_cli -i wlan0 save_config"
        os.system(cmd)
