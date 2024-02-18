# Pi code to use a OLED screen
import machine
import ssd1306

def testOled():

    sda = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)
    scl = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)
    i2c = machine.I2C(0,sda=sda, scl=scl, freq=400000)

    print('Scan i2c bus...')
    devices = i2c.scan()

    if (len(devices) == 0):
        print("No i2c device!")
    else:
        print('i2c devices found:',len(devices))
        
    for device in devices:
        print("Decimal address: ",device," | Hexa address: ",hex(device))
        
    print("creating oled")
    oled = ssd1306.SSD1306_I2C(128, 32, i2c, device)

    print("oled created")
    oled.fill(0)

    oled.text('Armed!', 40, 20, 1)

    print("about to call show")
    oled.show()


try:
    testOled()
finally:
    print("exiting from finally")