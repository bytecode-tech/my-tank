import sys
import Adafruit_DHT

def read_temp():
    return Adafruit_DHT.read_retry(22, 4)