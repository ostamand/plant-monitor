import machine
from machine import ADC
from neopixel import NeoPixel

import adafruit_io as io
from plant_monitor import Board
from secrets import secrets
from constants import * 

"""Setup 

"""
# adafruit io client
client=io.Client(secrets['ssid'], 
                 secrets['password'], 
                 secrets['aio_username'], 
                 secrets['aio_key']
                )
client.connect()
# plant monitor board 
board = Board()

"""Main 
    - check calibration pin
    - if delay, get moisture & send data to io
    - update neopixel animation depending on moisture level imp
"""
current_mode = Board.NORMAL
last_upd_time = 0
while True:
    # update current mode 
    if current_mode == Board.NORMAL and board.is_calibration():
        print('set to calibration mode') 
        current_mode = Board.CAL
    elif current_mode == Board.CAL and not board.is_calibration(): 
        print('set to normal mode') 
        current_mode = Board.NORMAL

    # normal mode
    if current_mode == Board.NORMAL:
        now = time.ticks_ms()
        delta = time.ticks_diff(now, last_upd_time)
        if delta > delay_upd*1000:
            last_upd_time = now 
            is_below, value = board.is_moisture_below_thresh()
            client.send_data('moisture-sensor', value)
            if is_below:
                board.np_animate_update()
            else: 
                board.np_off()

    # calibration mode. nothing to do on update 








