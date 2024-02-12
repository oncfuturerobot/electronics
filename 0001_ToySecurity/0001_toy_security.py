from pygame import mixer 
import os
import RPi.GPIO as GPIO
import time
TRIG = 24
ECHO = 23
import time
from time import sleep


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, GPIO.LOW)
    sleep(1)

def distance():

    print("distance 1")
    GPIO.output(TRIG,GPIO.LOW)
    time.sleep(0.0001)
    
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    print("distance 2")

    startTime = time.time()
    pulse_send = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_send = time.time()
    print("distance 2a pulse_send=",pulse_send)
    time1 = time.time()

    print("GPIO.input(ECHO)=",GPIO.input(ECHO))
    startTime = time.time()
    shouldStop = False
    while GPIO.input(ECHO) != 0 and not shouldStop:
        pulse_received= time.time()
        eTime = time.time() - startTime
        if (eTime > 1):
            print("too much time!")
            shouldStop = True

    print("done.. GPIO.input(ECHO)=",GPIO.input(ECHO), "shouldStop=",shouldStop)
    time2 = time.time()

    print("distance 3")

    during = time2 - time1
    return during * 340 / 2 * 100


def delayMicroseconds(microseconds):
    time.sleep(microseconds / 1000000)

def distanceHiLetgo():

    print("distance 1")
    GPIO.output(TRIG,0)
    delayMicroseconds(2)
    
    GPIO.output(TRIG, 1)
    delayMicroseconds(20)
    GPIO.output(TRIG, 0)

    print("distance 2")

    while GPIO.input(ECHO) == 0:
        a = 0

    print("distance 2a")
    time1 = time.time()

    print("GPIO.input(ECHO)=",GPIO.input(ECHO))
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    print("distance 3")

    during = time2 - time1
    return during * 340 / 2 * 100

user = os.getlogin()
user_home = os.path.expanduser(f'~{user}')

mixer.init()

def main():
    mixer.music.load(f'{user_home}/code/raphael-kit/music/my_music.mp3')
    mixer.music.set_volume(0.7)
    #mixer.music.play()
    
    print("about to do distance")
    while True:
        dis = distance()
        print ('Distance: %.2f' % dis )
        time.sleep(0.3)

def destroy():
    mixer.music.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        main()
    except KeyboardInterrupt:
        destroy()

