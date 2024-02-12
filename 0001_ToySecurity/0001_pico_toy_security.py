from machine import Pin
import utime


TRIG_PIN = 13
ECHO_PIN = 12

trigPin = Pin(TRIG_PIN, mode=Pin.OUT, value=0)
echoPin = Pin(ECHO_PIN,mode=Pin.IN)


#time.sleep(2)

utime.sleep_us(2)
trigPin.high()
#time.sleep(0.00001)
utime.sleep_us(5)
trigPin.low()

while echoPin.value()==0:
    pulse_send=utime.ticks_us()
    #print("SENT ",pulse_send)

while echoPin.value()==1:
    pulse_received=utime.ticks_us()
    #print("RECEIVED ",pulse_received)

pulse_duration = pulse_received - pulse_send
pulse_duration_orig = pulse_duration
#pulse_duration = round(pulse_duration/2,2)

#distance = 34000*pulse_duration
timepassed = pulse_received - pulse_send
distance = (timepassed * 0.0343) / 2

print("Object is at",distance,"cm from the sensor send=",round(pulse_send,2), " receive=",pulse_received, "duration=",pulse_duration," orig=",pulse_duration_orig)




