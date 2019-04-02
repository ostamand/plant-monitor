import network 
import urequests as requests

"""Adafruit IO REST client

"""
class Client:

    def __init__(self, ssid, password, aio_username, aio_key):
        self.ssid = ssid 
        self.password = password
        self.aio_username = aio_username
        self.aio_key = aio_key

    """Connect to the wifi
    """
    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print('connecting to network...')
            self.wlan.connect(self.ssid, self.password)
            while not wlan.isconnected():
                pass
        print('network config:', self.wlan.ifconfig())

    """Send data thru rest api
    """
    def send_data(self, feed_key, value):
        # check wifi first
        if not self.wlan.isconnected():
            self.connect()
        url = "https://io.adafruit.com/api/v2/{}/feeds/{}/data.json".format(self.aio_username, feed_key)
        headers = {'X-AIO-Key': self.aio_key,
                   'Content-Type': 'application/json' }
        data = '{"value": '
        data += '{}'.format(value)
        data += '}'
        r = requests.post(url, data=data, headers=headers)
        #results = r.json()
        #print(results)
        return r.status_code
