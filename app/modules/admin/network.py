from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
import threading
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

def scan():
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.1)  # let reactor start

    driver = WpaSupplicantDriver(reactor)
    supplicant = driver.connect()
    interface = supplicant.get_interface('wlan0')

    scan_results = interface.scan(block=True)
    networks = []

    for bss in scan_results:
        networks.append(WifiNetwork(bss=bss))

    reactor.stop()
    return networks

def saved_networks():
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.1)  # let reactor start

    driver = WpaSupplicantDriver(reactor)
    supplicant = driver.connect()
    interface = supplicant.get_interface('wlan0')

    results = interface.get_networks()
    networks = []
    for network in results:
        networks.append(Network(network=network))

    return networks


def save_network(name: str, password: str, enabled: bool, priority: str):
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.1)  # let reactor start

    driver = WpaSupplicantDriver(reactor)
    supplicant = driver.connect()
    interface = supplicant.get_interface('wlan0')

    network_config = { }
    sample_network_cfg['psk'] = password
    sample_network_cfg['ssid'] = name
    sample_network_cfg['key_mgmt'] = "WPA-PSK"

    return interface.add_network(network_config)

def network_info(name):
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.1)  # let reactor start

    driver = WpaSupplicantDriver(reactor)
    supplicant = driver.connect()
    interface = supplicant.get_interface('wlan0')

    results = interface.get_networks()

    found_network = None
    for network in results:
        ssid = network.get_properties().get('ssid')
        if ssid.lower() == name.lower():
            found_network = Network(network=network)
    
    return found_network

def delete_network(name):
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.1)  # let reactor start

    driver = WpaSupplicantDriver(reactor)
    supplicant = driver.connect()
    interface = supplicant.get_interface('wlan0')

    results = interface.get_networks()

    for network in results:
        ssid = network.get_properties().get('ssid')
        if ssid.lower() == name.lower():
            interface.remove_network(network.get_path())
            break
    
def activate_network(name):
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.1)  # let reactor start

    driver = WpaSupplicantDriver(reactor)
    supplicant = driver.connect()
    interface = supplicant.get_interface('wlan0')

    results = interface.get_networks()

    for network in results:
        ssid = network.get_properties().get('ssid')
        if ssid.lower() == name.lower():
            interface.select_network(network.get_path())
            break

def active_network():
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.1)  # let reactor start

    driver = WpaSupplicantDriver(reactor)
    supplicant = driver.connect()
    interface = supplicant.get_interface('wlan0')

    network = interface.get_current_network()
    return Network(network=network)
