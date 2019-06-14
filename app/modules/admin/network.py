from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
import threading
import time

class WifiNetwork():
    def __init__(self, *args, **kwargs):
        self.bssid = None
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
            self.channel = bss.get_channel()
            self.frequency = bss.get_frequency()
            self.mode = bss.get_mode()
            self.type = bss.get_network_type()
            self.privacy = bss.get_privacy()
            self.signal_dbm = bss.get_signal_dbm()
            self.signal_quality = bss.get_signal_quality()
            

def scan():
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.5)  # let reactor start

    driver = WpaSupplicantDriver(reactor)

    supplicant = driver.connect()

    interface = supplicant.get_interface('wlan0')

    scan_results = interface.scan(block=True)
    networks = []

    for bss in scan_results:
        networks.append(WifiNetwork(bss=bss))

    reactor.stop()
    return networks