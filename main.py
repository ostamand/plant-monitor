import machine
from machine import ADC
from neopixel import NeoPixel
import time

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
board = Board(thresh=thresh_moisture, np_color=neopixel_color, thresh_n=thresh_n)

"""Main 
"""
last_upd_time = 0
while True:
    # update current mode 
    if not board.is_calibration_mode() and board.is_calibration_on():
        print('set to calibration mode') 
        board.set_to_calibration_mode()
    elif board.is_calibration_mode() and not board.is_calibration_on(): 
        print('set to normal mode') 
        board.set_to_normal_mode()

    # normal mode
    if not board.is_calibration_mode():
        now = time.ticks_ms()
        delta = time.ticks_diff(now, last_upd_time)
        print('delta_t: {}'.format(delta))
        if delta > delay_upd*1000:
            last_upd_time = now 
            is_below, value = board.is_moisture_below_thresh()
            print('moisture {}'.format(value))
            client.send_data('moisture-sensor', value)
            if board.is_normal_mode() and is_below:
                print('set to below thresh mode')
                board.set_to_below_thresh_mode()
            elif board.is_below_mode() and not is_below: 
                print('set to normal mode')
                board.set_to_normal_mode()
        board.np_animate_update()

    # calibration mode. nothing to do on update 








