import os
import RPi.GPIO as GPIO
from multiprocessing import Process
from app import create_app
from gpiozero import DistanceSensor
import time

app = create_app()

if __name__ == "__main__":
    print 'Setting up board'
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)