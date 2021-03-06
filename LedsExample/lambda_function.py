import urllib2
import json

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.endpoint"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])

    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])

    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    session_attributes = {}
    card_title = "BART"
    speech_output = "This is the system to control ESP. "

    reprompt_text = "Tell me what to do"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def build_response(session_attributes, speechlet_response):
    return {"version": "1.0","sessionAttributes": session_attributes,"response": speechlet_response}

def on_intent(intent_request, session):
    session_attributes = {}
    card_title = "BART"
    speech_output = "Your desires are orders."

    reprompt_text = "Tell me what to do"
    should_end_session = False
    aws_mqtt()
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
}


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
}

def aws_mqtt():
    import paho.mqtt.client as paho
    import os
    import socket
    import ssl
    from time import sleep
    from random import uniform

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
    mqttc.publish("TriggerLeds",trigger, qos=1)
