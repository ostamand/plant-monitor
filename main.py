import machine
from machine import ADC
from neopixel import NeoPixel
import network

import adafruit_io as io
from secrets import secrets

# setup 

# moisture sensor pwr connected to GPI14. 
pwr_sensor = machine.Pin(14, machine.Pin.OUT)

# moisture sensor analog signal on ADC 
# moisture_sensor.read() 0-1024 
moisture_sensor = ADC(0)

# calibration mode pin GPIO2 
calibration_pin = machine.Pin(2, machine.Pin.IN)
#print(calibration_pin.value())

# neopixel   
# feather can output 500 mA max.
# selected color: (33, 23, 125)
# 110 mA at 25% 
# 370 mA at 100%
np_pin = machine.Pin(0, machine.Pin.OUT)
np = NeoPixel(np_pin, 30)   # create NeoPixel driver on GPIO0 for 8 pixels
#np[0] = (255, 0, 255)       # set the first pixel to white
#np.write()                  # write data to all pixels
#r, g, b = np[0]             # get first pixel colour

# adafruit io client

client=io.Client(secrets['ssid'], 
                 secrets['password'], 
                 secrets['aio_username'], 
                 secrets['aio_key']
                )
client.connect()
client.send_data('moisture-sensor', 100)




