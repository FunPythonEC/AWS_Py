import machine
import neopixel
import random

numero_leds=39
pin_salida=19

np = neopixel.NeoPixel(machine.Pin(pin_salida), numero_leds)
#Red
def ledsred():
    for led in range(0,numero_leds,1):
        np[led]=(255,0,0)
        np.write()

def ledsblue():
    for led in range(0,numero_leds,1):
        np[led]=(0,0,255)
        np.write()

def ledsyellow():
    for led in range(0,numero_leds,1):
        np[led]=(255,255,0)
        np.write()

def ledson():
    for led in range(0,numero_leds,1):
        np[led]=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        np.write()

def ledsoff():     
    for led in range(0,numero_leds,1):
        np[led]=(0,0,0)
        np.write()


 
