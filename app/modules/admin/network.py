from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
import threading
import time

def scan():
    reactor = SelectReactor()
    threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
    time.sleep(0.5)  # let reactor start

    driver = WpaSupplicantDriver(reactor)

    supplicant = driver.connect()

    interface = supplicant.get_interface('wlan0')

    scan_results = interface.scan(block=True)
    ssids = {}

    for bss in scan_results:
        ssid = bss.get_ssid()
        if ssid not in ssids:
            ssids[ssid] = bss.to_dict()

    reactor.stop()
    return ssids
