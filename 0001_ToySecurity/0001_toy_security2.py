from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, LED
import time
from time import sleep

# ----------------------------------------------------------
# Init
# ----------------------------------------------------------

ultrasonic = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)

# ----------------------------------------------------------
# Reduce Jitter by using PiGPIOFactor
# sudo systemctl enable pigpiod
# sudo sudo systemctl start pigpiod
# sudo pigpiod
# ----------------------------------------------------------
Device.pin_factory = PiGPIOFactory('127.0.0.1')


# ----------------------------------------------------------
# Setup
# ----------------------------------------------------------

def setup():
    pass


def destroy():
    pass

# ----------------------------------------------------------
# Main body
# ----------------------------------------------------------
def main():
    while True: 
        print("distance =",ultrasonic.distance*1000)
        sleep(0.2)
        

if __name__ == '__main__':
    try:
        setup()
        main()
    except KeyboardInterrupt:
        destroy()
