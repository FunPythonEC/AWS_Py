import machine
import network
import time
from umqtt.robust import MQTTClient
import ledscontrol as leds

def cb(topic, msg):
    if msg==b'11':
        leds.ledson()
        print(msg)
    if msg==b'12':
        leds.ledsoff()
        print(msg)
    if msg==b'13':
        leds.ledsred()
        print(msg)
    if msg==b'14':
        leds.ledsblue()
        print(msg)
    if msg==b'15':
        leds.ledsyellow()
        print(msg)

HOST = b'endpoint.iot.us-east-1.amazonaws.com'
TOPIC = bytes('PruebaESP32', 'utf-8')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASS")
time.sleep(5)

cert="/cert/cert.pem.crt"
key="/cert/private.pem.key"
root="/cert/root_ca.pem"

with open(cert, 'rb') as f:
    certf = f.read()
print(certf)

with open(key, 'rb') as f:
    keyf = f.read()
print(keyf)

with open(root, 'rb') as f:
    rootf = f.read()
print(rootf)

time.sleep(5)

def run():
    global state
    global connection
    
    connection = MQTTClient(client_id=TOPIC, server=HOST, port=8883, ssl=True, ssl_params={"cert":certf, "key":keyf})
    connection.connect()
    connection.set_callback(cb)                    
    connection.subscribe(b'LedsState')

    while True:
        try:
            connection.wait_msg()
        except Exception:
            pass
run()
