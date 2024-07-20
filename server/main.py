import network
import time
import socket
import machine  # Import the machine module
import json  # Import json for converting dictionaries to JSON strings

led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
wlan = network.WLAN(network.STA_IF)
queue = []

def send_response(conn, status, payload):
    status_str = ""
    if status == 200:
        status_str = "OK"
    else:
        status_str = "Not Found"
    
    header = f'HTTP/1.0 {status} {status_str}\r\nContent-type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
    conn.send(header)
    conn.send(json.dumps(payload))  # Convert the payload to a JSON string
    conn.close()
    
def appendToQueue(x):
    global queue
    current_time = time.time() * 1000
    queue.append({"data": x, "timestamp": current_time})

def ap_mode(ssid, password):
    global queue
    # Pico wird selbst zum Access Point
    print('Access-Point wird aufgebaut')
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=ssid, password=password)
    wlan.active(True)
    
    while not wlan.active():
        pass
    print('Access Point ist nun erreichbar')
    print('IP Adresse:: ' + wlan.ifconfig()[0])
    
    # Hier würde die serverseitige Socketbehandlung stattfinden
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creating socket object
    s.bind(('', 80))
    s.listen(5)
    
    # _thread.start_new_thread(pico_client_request,(1,))

    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)
         
            try:
                request = request.split()[1]
            except IndexError:
                pass
            print(request)
            if request == "/":
                send_response(conn, 200, {})
            elif request == "/queue":
                send_response(conn, 200, queue)
            elif request == "/clear":
                queue = []
                send_response(conn, 200, {})
            elif request == "/1":
                appendToQueue(1)
                send_response(conn, 200, {})
            elif request == "/2":
                appendToQueue(2)
                send_response(conn, 200, {})
            elif request == "/3":
                appendToQueue(3)
                send_response(conn, 200, {})
            elif request == "/4":
                appendToQueue(4)
                send_response(conn, 200, {})
            elif request == "/5":
                appendToQueue(5)
                send_response(conn, 200, {})
            else:
                send_response(conn, 404, {})
                 
        except OSError as e:
            conn.close()  # Corrected the variable name to conn
            print('connection closed')

ap_mode('PicoPico', 'password')


