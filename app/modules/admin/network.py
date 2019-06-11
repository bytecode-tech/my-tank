from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
import threading
import time

reactor = SelectReactor()
threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()
time.sleep(0.1)  # let reactor start

driver = WpaSupplicantDriver(reactor)

supplicant = driver.connect()

interface = supplicant.get_interface('wlan0')

def scan():
    scan_results = interface.scan(block=True)
    ssids = []
    
    for bss in scan_results:
        ssids.append(bss.get_ssid())
    
    return ssids
