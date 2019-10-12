import sys
import Adafruit_DHT
import smbus
import time
import logging

_LOGGER = logging.getLogger(__name__)

def read_temp():
    return read_dht_22()

def read_dht_22():
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    temperature = 9.0/5.0 * temperature + 32
    return {'temperature': temperature, 'humidity': humidity}

def read_sht_30():
    try:
        # Get I2C bus
        bus = smbus.SMBus(1)

        # SHT30 address, 0x44(68)
        # Send measurement command, 0x2C(44)
        #		0x06(06)	High repeatability measurement
        bus.write_i2c_block_data(0x44, 0x2C, [0x06])

        time.sleep(0.5)

        # SHT30 address, 0x44(68)
        # Read data back from 0x00(00), 6 bytes
        # cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        data = bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
        fTemp = cTemp * 1.8 + 32
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
        return {'temperature': fTemp, 'humidity': humidity}
    except:
        _LOGGER.exception("SHT-30 not reporting")
    finally:
        return None