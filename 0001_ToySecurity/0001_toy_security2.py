from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LightSensor
from gpiozero import Device, LED
import time
from time import sleep

# ----------------------------------------------------------
# Reduce Jitter by using PiGPIOFactor
# sudo systemctl enable pigpiod
# sudo sudo systemctl start pigpiod
# sudo pigpiod
# ----------------------------------------------------------
Device.pin_factory = PiGPIOFactory('127.0.0.1')

# ----------------------------------------------------------
# Init
# ----------------------------------------------------------
print("Warming up sensors...")

ultrasonic = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)
#ultrasonic = DistanceSensor(echo=23, trigger=24)
laser_1_sensor = LightSensor(16)

sleep(1)

# ----------------------------------------------------------
# Setup
# ----------------------------------------------------------

def setup():
    pass


def destroy():
    laser_1_sensor.close()
    ultrasonic.close()

# ----------------------------------------------------------
# Main body
# ----------------------------------------------------------
def main():
    while True: 
        print("distance =",ultrasonic.distance*1000, "mm laser=",laser_1_sensor.value)
        sleep(0.2)
        

if __name__ == '__main__':
    try:
        setup()
        main()
    except KeyboardInterrupt:
        destroy()
