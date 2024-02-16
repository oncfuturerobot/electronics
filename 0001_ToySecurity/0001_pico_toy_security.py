import machine
from machine import Pin
import utime


# ---------------------------------------------------------
# Pins
# ---------------------------------------------------------

TRIG_PIN = 13
ECHO_PIN = 12

trigPin = Pin(TRIG_PIN, mode=Pin.OUT, value=0)
echoPin = Pin(ECHO_PIN,mode=Pin.IN)

# ---------------------------------------------------------
# LEDs
# ---------------------------------------------------------

red_led = machine.Pin(16, machine.Pin.OUT)
blue_led = machine.Pin(15, machine.Pin.OUT)

red_led.off()
blue_led.off()

# ---------------------------------------------------------
# States
# ---------------------------------------------------------


class OverallState:
    OFF = 0
    WATCHING = 1
    ALARMING = 2
    
class AlarmingState:
    OFF = 0
    RED_LED_ON = 1
    BLUE_LED_ON = 2
   
    



# ---------------------------------------------------------
# State Change functions
# ---------------------------------------------------------

def change_overall_state(new_state):
    global overall_state,last_overall_state_change_time
    print("change_overall_state ",new_state)
    if new_state == OverallState.WATCHING :
         blue_led.on()
         red_led.off()
    elif new_state == OverallState.ALARMING:
         change_alarming_state(AlarmingState.RED_LED_ON)
         
    overall_state = new_state
    last_overall_state_change_time = utime.ticks_ms()
    
def change_alarming_state(new_state):
    global alarming_state,last_alarming_state_change_time 
    print("change_alarming_state",new_state)
    if new_state == AlarmingState.RED_LED_ON :
         red_led.on()
         blue_led.off()
    elif new_state == AlarmingState.BLUE_LED_ON:
         blue_led.on()
         red_led.off()
    elif new_state == AlarmingState.OFF:
         red_led.off()
         blue_led.off()
    
         
    alarming_state = new_state
    last_alarming_state_change_time = utime.ticks_ms()
    
# ---------------------------------------------------------
# State defaults
# ---------------------------------------------------------

overall_state = OverallState.OFF

last_overall_state_change_time = utime.ticks_ms()

alarming_state = AlarmingState.OFF

# ---------------------------------------------------------
# Ultrasonic sensor 
# ---------------------------------------------------------

def getDistance():
    global overall_state

    #print("getDistance")
    trigPin.low()
    utime.sleep_us(20000)
    trigPin.high()
    utime.sleep_us(5)
    trigPin.low()

    pulse_send=utime.ticks_us()
    pulse_received=utime.ticks_us()

    #print("wait for 0")
    while echoPin.value()==0:
        pulse_send=utime.ticks_us()

    #print("wait for 1")
    should_stop = False
    while echoPin.value()==1 and not should_stop:
        pulse_received=utime.ticks_us()
        if pulse_received - pulse_send > 200000:
            should_stop = True
            print("Timed out!")
            

    pulse_duration = pulse_received - pulse_send
    pulse_duration_orig = pulse_duration

    timepassed = pulse_received - pulse_send
    distance = (timepassed * 0.0343) / 2
    #distanceMM = distance * 10,2

    return distance


# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------


change_overall_state(OverallState.WATCHING)

while True:

    if overall_state == OverallState.WATCHING:
        distanceInMM = getDistance()
        if distanceInMM > 8:
            change_overall_state(OverallState.ALARMING)
    elif overall_state == OverallState.ALARMING:
        
        delta_time = utime.ticks_ms() - last_alarming_state_change_time
        if delta_time > 200:
            if alarming_state == AlarmingState.BLUE_LED_ON:
                change_alarming_state(AlarmingState.RED_LED_ON)
            else:
                change_alarming_state(AlarmingState.BLUE_LED_ON)
        else:
            
            print("not time yet delta=", delta_time , " utime.time()=",utime.time()," last_alarming_state_change_time=",last_alarming_state_change_time )
        
        distanceInMM = getDistance()
        #print("distanceInMM=",distanceInMM)
        if distanceInMM <= 8:
            change_overall_state(OverallState.WATCHING)
        
    
    #utime.sleep_us(2000)
    
    