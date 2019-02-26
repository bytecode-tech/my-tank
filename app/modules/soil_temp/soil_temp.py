from w1thermsensor import W1ThermSensor

def soil_temp():
    try:
        soil_sensor = W1ThermSensor()
        temp = soil_sensor.get_temperature(W1ThermSensor.DEGREES_F)
        return temp
    except:
        print('Soil sensor exception')
        raise