import machine
from machine import ADC
from neopixel import NeoPixel
import time

class Board:

    # mode: 0=normal, 1=calibration, 2=below thresh
    NORMAL = 0
    CAL = 1
    BELOW_THRESH = 2

    def __init__(self, thresh=300, np_color=(33,23,125):
        self.thresh = thresh
        self.np_color = np_color 

        # moisture sensor pwr connected to GPI14.
        self.pwr_sensor = machine.Pin(14, machine.Pin.OUT)

        # moisture sensor analog signal on ADC 
        self.moisture_sensor = ADC(0)

        # calibration mode pin GPIO2 
        self.calibration_pin = machine.Pin(2, machine.Pin.IN)

        np_pin = machine.Pin(0, machine.Pin.OUT)
        self.np = NeoPixel(np_pin, 30)   # create NeoPixel driver on GPIO0 for 8 pixels

    def get_moisture(self):
        self.pwr_sensor.on()
        time.sleep(1)
        value = self.moisture_sensor.read()
        self.pwr_sensor.off()
        return value

    def is_moisture_below_thresh(self):
        value = self.get_moisture()
        return (value < self.thresh, value)

    def is_calibration(self):
        return self.calibration_pin.value()

    def is_np_off(self):
        pass

    def np_off(self):
        pass

    # will animate neopixels until the moisture is below the thresh
    # feather can output 500 mA max.
    # selected color: (33, 23, 125)
    # 110 mA at 25% 
    # 370 mA at 100%
    def np_animate_update(self):
        #np[0] = (255, 0, 255)       # set the first pixel to white
        #np.write()                  # write data to all pixels
        #r, g, b = np[0]             # get first pixel colour
        pass 

