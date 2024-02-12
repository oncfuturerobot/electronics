import machine
import utime

red_led = machine.Pin(16, machine.Pin.OUT)
blue_led = machine.Pin(15, machine.Pin.OUT)

while True:
    red_led.on()
    blue_led.off()
    utime.sleep(1.1)
    red_led.off()
    blue_led.on()
    utime.sleep(3.1)

