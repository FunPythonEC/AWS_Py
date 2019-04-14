import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

awshost = "endpoint.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "TriggerLeds"
thingName = "TriggerLeds"
caPath = "cert/root_ca.pem"
certPath = "cert/cert.pem.crt"
keyPath = "cert/private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()
trigger="1"
for i in range(10):
    mqttc.publish("TriggerLeds",trigger, qos=1)
    sleep(1)
