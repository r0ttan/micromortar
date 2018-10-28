from microbit import display, button_a, button_b, sleep, accelerometer, Image
import math, radio
from random import randint

minx = 460
maxx = 1075
g = 9.82
x = 0
v0 = 100
angcount = 0
hitarea = 30

radio.config(channel=57)
radio.on()
tempx = randint(minx, maxx)
alive = True

def getangle():
    return math.radians(accelerometer.get_y()/11.38), accelerometer.get_z()

while x == 0:
    r = radio.receive()
    if r != None:
        try:
            x = int(r)
            radio.send("READY")
        except ValueError:
            pass
        if r == "READY":
            x, tempx = tempx, x
            radio.send("READY")
            break
    radio.send(str(tempx))
display.show("3 2 1 ")


while alive:
    h = radio.receive()
    angcount += 1
    if angcount >= 700:
        angle, zangle = getangle()
    velocity = 0
    vdelta = 1
    while button_a.is_pressed():
        velocity += 1*vdelta
        display.show(velocity)
        sleep(400)
        if velocity==4 or velocity==0:
            vdelta = vdelta*(-1)
    v0 = v0 + velocity
    if h == 'H':
        alive = False
        display.show(Image.ASLEEP, wait=True, clear=False)
        break
    elif h == 'WO':
        break;
    if button_a.was_pressed():
        y = (x*(math.tan(angle)))-(g*(x**2))/((2*(v0**2))*((math.cos(angle))**2))
        display.show("F F F")
        sleep(600)
        if y < -hitarea:
            display.scroll("long", delay=95, wait=False)
        elif y > hitarea:
            display.scroll("short", delay=95, wait=False)
        else:
            radio.send('H')
            display.show("*")
            display.scroll("HIT")
            display.show("*")
    elif button_b.was_pressed():
        alive = False
        radio.send('WO')
        break

if alive:
    display.scroll("WINNER")
    display.show(Image.HAPPY)
else:
    display.scroll("LOSER")
    display.show(Image.SAD)
