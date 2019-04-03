import machine
from machine import ADC
from neopixel import NeoPixel
import time

class Board:

    # mode: 0=normal, 1=calibration, 2=below thresh
    NORMAL = 0
    CAL = 1
    BELOW_THRESH = 2

    def __init__(self, thresh=300, thresh_n=5, np_color=(33,23,125)):
        self.thresh = thresh
        self.np_color = np_color
        self.thresh_n = thresh_n

        # current count below thresh
        self.count_thresh = None 

        # moisture sensor pwr connected to GPI14.
        self.pwr_sensor = machine.Pin(14, machine.Pin.OUT)

        # moisture sensor analog signal on ADC 
        self.moisture_sensor = self.moisture_sensor = ADC(0)

        # calibration mode pin GPIO2 
        self.calibration_pin = machine.Pin(2, machine.Pin.IN)

        np_pin = machine.Pin(0, machine.Pin.OUT)
        self.np_n = 30
        self.np = NeoPixel(np_pin, self.np_n)
        self._is_np_on = None 

        self.current_mode = None 
        self.set_to_normal_mode()

    def get_moisture(self):
        self.pwr_sensor.on()
        time.sleep(1)
        value = self.moisture_sensor.read()
        self.pwr_sensor.off()
        return value

    def is_moisture_below_thresh(self):
        value = self.get_moisture()
        if value < self.thresh:
            self.count_thresh += 1 
        else:
            if self.count_thresh > 0:
                self.count_thresh -= 1  
        return (self.count_thresh > self.thresh_n, value)
    
    def is_normal_mode(self):
        return self.current_mode == Board.NORMAL

    def is_calibration_mode(self):
        return self.current_mode == Board.CAL

    def is_below_mode(self):
        return self.current_mode == Board.BELOW_THRESH

    # led on = calibration mode 
    def is_calibration_on(self):
        return not self.calibration_pin.value()

    def set_to_calibration_mode(self):
        # sensor always on 
        self.pwr_sensor.on()
        # np always off 
        self.np_off()
        self.current_mode = Board.CAL

    def set_to_normal_mode(self):
        self.count_thresh = 0
        self.pwr_sensor.off()
        self.np_off()
        self.current_mode = Board.NORMAL

    def set_to_below_thresh_mode(self):
        # temp to be updated 
        for i in range(self.np_n):
            self.np[i] = self.np_color
        self.np.write()
        self._is_np_on = True 
        self.current_mode = Board.BELOW_THRESH

    def is_np_off(self):
        return not self._is_np_on

    def np_off(self):
        for i in range(self.np_n):
            self.np[i] = (0,0,0) 
        self.np.write()
        self._is_np_on = False 

    # will animate neopixels until off is called 
    # feather can output 500 mA max.
    # selected color: (33, 23, 125)
    # 110 mA at 25% 
    # 370 mA at 100%
    def np_animate_update(self):
        pass



