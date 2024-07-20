import os, wifi
import time
from digitalio import *
import board
import busio
import socketpool
import ssl

import adafruit_requests

# Initialize a requests session
pool = socketpool.SocketPool(wifi.radio)
http = adafruit_requests.Session(pool, ssl.create_default_context())


questionButton = DigitalInOut(board.GP14)
questionButton.direction = Direction.INPUT
questionButton.pull = Pull.UP

explainButton = DigitalInOut(board.GP12)
explainButton.direction = Direction.INPUT
explainButton.pull = Pull.UP

louderButton = DigitalInOut(board.GP5)
louderButton.direction = Direction.INPUT
louderButton.pull = Pull.UP

againButton = DigitalInOut(board.GP2)
againButton.direction = Direction.INPUT
againButton.pull = Pull.UP

pointerButton = DigitalInOut(board.GP0)
pointerButton.direction = Direction.INPUT
pointerButton.pull = Pull.UP

WLAN_SSID = "PicoPico"
WLAN_PWD = 'password'

reconnects = 0

led_onboard = DigitalInOut(board.LED)
led_onboard.direction = Direction.OUTPUT


response =  0
on_going = set()


def connect_to_wifi(reconnects=0):
    # Check if already connected
    try:
        wifi.radio.connect(ssid=WLAN_SSID, password=WLAN_PWD)
    except ConnectionError:
        print(f"Trying to connect ({reconnects})")
        time.sleep(reconnects*500)
        connect_to_wifi(reconnects+1)
        if reconnects >=10:
            print("Connection not available")
    
    print("Connected to Wi-Fi succesfully")

def send(code):
    global on_going
    apiUrl = "http://192.168.4.1/"
    if code in on_going:
        return
    try:
        on_going.add(code)
        print("Send it:"+ str(code))
        
        if code == 1:
            response = http.post(apiUrl+str(code))
        elif code == 2:
            response = http.post(apiUrl+str(code))
        elif code == 3:
            response = http.post(apiUrl+str(code))
        elif code == 4:
            response = http.post(apiUrl+str(code))
        elif code == 5:
            response = http.post(apiUrl+str(code))
        print(response)
        if response.status_code == 200:
            print("yippie")
        else:
            print("boooo")
        response.close()
            
    except OSError:
        print("ERROR")
    
    finally:
        on_going.remove(code)

if __name__ == "__main__":

    connect_to_wifi() 

    while True:
        # HTTP-Request senden0    
        if questionButton.value == 0:
            send(1)
        if explainButton.value == 0:
            send(2)
        if louderButton.value == 0:
            send(3)
        if againButton.value == 0:
            send(4)
        if pointerButton.value == 0:
            send(5)
        #time.sleep(2)
        #send(5)


        





