import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 24
ECHO_PIN = 23

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.output(TRIG_PIN,GPIO.LOW)

#time.sleep(2)

GPIO.output(TRIG_PIN, GPIO.HIGH)
time.sleep(0.00001)

GPIO.output(TRIG_PIN,GPIO.LOW)

while GPIO.input(ECHO_PIN)==0:
    pulse_send=time.time()
    #print("SENT")

while GPIO.input(ECHO_PIN)==1:
    pulse_received=time.time()
    #print("RECEIVED")

pulse_duration = pulse_received - pulse_send
pulse_duration_orig = pulse_duration
#pulse_duration = round(pulse_duration/2,2)

distance = 34000*pulse_duration
print("Object is at",distance,"cm from the sensor send=",round(pulse_send,2), " receive=",pulse_received, "duration=",pulse_duration," orig=",pulse_duration_orig)

GPIO.cleanup()


