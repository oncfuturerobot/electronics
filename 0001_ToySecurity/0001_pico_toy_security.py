import machine
from machine import Pin
import utime
from picozero import Speaker
import ssd1306

# ---------------------------------------------------------
# Pins
# ---------------------------------------------------------

TRIG_PIN = 13
ECHO_PIN = 12

trigPin = Pin(TRIG_PIN, mode=Pin.OUT, value=0)
echoPin = Pin(ECHO_PIN,mode=Pin.IN)


# ---------------------------------------------------------
# Buzzer
# ---------------------------------------------------------

speaker = Speaker(0)


# ---------------------------------------------------------
# LEDs
# ---------------------------------------------------------

red_led = machine.Pin(16, machine.Pin.OUT)
blue_led = machine.Pin(15, machine.Pin.OUT)

red_led.off()
blue_led.off()

# ---------------------------------------------------------
# Display
# ---------------------------------------------------------

sda = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)
scl = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)
i2c = machine.I2C(0,sda=sda, scl=scl, freq=400000)
display = None

def InitDisplay():
    global display
    devices = i2c.scan()

    if (len(devices) == 0):
        print("No i2c device!")
    else:
        print('i2c devices found:',len(devices))
        
    for device in devices:
        print("i2c Decimal address: ",device," | Hexa address: ",hex(device))
        
    display = ssd1306.SSD1306_I2C(128, 32, i2c, device)
    display.fill(0)
    display.text('Booting...', 40, 20, 1)
    display.show()

def ChangeDisplay():
    global overall_state
    display.fill(0)
    
    if overall_state == OverallState.WATCHING :
        display.text('Armed...', 40, 20, 1)    
    elif overall_state == OverallState.ALARMING:
        display.text('ALERT THIEF!', 20, 20, 1)

    display.show()


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
         change_alarming_state(AlarmingState.OFF)
    elif new_state == OverallState.ALARMING:
         change_alarming_state(AlarmingState.RED_LED_ON)
         
    overall_state = new_state
    last_overall_state_change_time = utime.ticks_ms()
    ChangeDisplay()
    
def change_alarming_state(new_state):
    global alarming_state,last_alarming_state_change_time 
    print("change_alarming_state",new_state)
    if new_state == AlarmingState.RED_LED_ON :
         red_led.on()
         blue_led.off()
         speaker.play('g5', 0.5,wait=False)
    elif new_state == AlarmingState.BLUE_LED_ON:
         blue_led.on()
         red_led.off()
         speaker.play('a3', 0.5,wait=False)
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
def mainLoop():

    global overall_state,alarming_state
    change_overall_state(OverallState.WATCHING)

    #for i in range(2000, 5000, 100):
    #    speaker.play(i, 0.05) # short duration
        
    while True:

        if overall_state == OverallState.WATCHING:
            distanceInMM = getDistance()
            if distanceInMM > 8:
                change_overall_state(OverallState.ALARMING)
            else:
                utime.sleep_us(2000)
        elif overall_state == OverallState.ALARMING:
            
            delta_time = utime.ticks_ms() - last_alarming_state_change_time
            if delta_time > 200:
                if alarming_state == AlarmingState.BLUE_LED_ON:
                    change_alarming_state(AlarmingState.RED_LED_ON)
                else:
                    change_alarming_state(AlarmingState.BLUE_LED_ON)
            
            distanceInMM = getDistance()
            #print("distanceInMM=",distanceInMM)
            if distanceInMM <= 8:
                change_overall_state(OverallState.WATCHING)
            
        
        
    
    
try:
    InitDisplay()
    mainLoop()
finally:
    speaker.off()
    blue_led.off()
    red_led.off()
    print("goodbye from finally!")
    
    