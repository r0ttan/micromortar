from microbit import display, button_a, button_b, sleep, accelerometer, Image, reset
import math, radio
from random import randint

minx = 460      #minimum distance between micro mortars
maxx = 1075     #max distance
g = 9.82        #gravity
x = 0           #virtual distance between micro mortars, negotiated b4 start
v0 = 100        #initial fire velocity
angcount = 0
hitarea = 38    #"explosion radius", hit within this distance will count
r = "EMPTY"     #string for distance negotiation

radio.config(channel=57)
radio.on()
tempx = randint(minx, maxx)     #this micro mortars distance suggestion
alive = True

def getangle():
    """ Accelerometer y output for first quadrant range 0-1024 """
    """    ~11.378 steps/degree (1024 steps / 90 degrees )   """
    return math.radians(accelerometer.get_y()/11.378), accelerometer.get_z()   #translate y angle to radians, z for backward shooting check (z should always be negative or zero if shooting straight up)

""" Negotiate range between mortars """
while x == 0:
    r = radio.receive()
    if r != None:  #got a message from other mortar
        try:
            x = int(r)    #check if int was received, distance negotiated, using other mortars suggestion
            radio.send("READY") #signal ready to start
        except ValueError:
            pass
        if r == "READY" and x == 0:   #Only happens if other mortar took our x, set my x to earlier sent x.
            x, tempx = tempx, x     #distance negotiated, using this mortars suggestion
            radio.send("READY")
            break
    radio.send(str(tempx))          #send distance suggestion
    display.show("zz", wait=False)
display.show("3 2 1 ")              #count down to start


while alive:            #this mortar is not yet hit
    h = radio.receive()
    angcount += 1
    if angcount >= 400:   #slow down angle checks without blocking execution
        angle, zangle = getangle()
        display.show("A")       # Alive
        sleep(500)
        display.set_pixel(0,0,8)
        a_deg = accelerometer.get_y()/11.4  #get approximate angle for display purpose
        a_bin = bin(int(a_deg))             #Convert whole degrees to binary as string e.g. 3 = "0b11"
        for n, v in enumerate(a_bin[2:]):
            display.set_pixel(n, 3, v*8)    #Visualize angle in binary notation (led on = 1)
        #display.show(accelerometer.get_y()/11.4, delay=450)
        sleep(200)
    velocity = 0
    vdelta = 1      #used for trimming velocity change while aiming
    while button_a.is_pressed():    #release button a when velocity is desired value
        velocity += 1*vdelta
        display.show(velocity)
        sleep(370)
        if velocity==5 or velocity==1:  #time to change count direction
            vdelta = vdelta*(-1)
    velocity = v0 + velocity
    if button_a.was_pressed():      #trigger pressed!
        y = (x*(math.tan(angle)))-(g*(x**2))/((2*(velocity**2))*((math.cos(angle))**2))   #calculate hight of virtual projectile when reaching negotiated distance
        display.show("F F ")        #Firing, stand by.
        sleep(500)
        if y < -hitarea:            # projectile would be below zero (the x-axis plane) at correct distance, and outside hit area, too short
            display.scroll("short", delay=95, wait=False)
        elif y > hitarea:           # projectile above hit area at correct distance, too long
            display.scroll("long", delay=95, wait=False)
        else:                       #Confirmed hit!
            radio.send('H')         #Tell opponent it got hit.
            display.show("*")
            display.scroll("HIT")
            display.show("*")
            break
    elif button_b.was_pressed():    # Waive the white flag and give up.
        alive = False
        radio.send('WO')            # Loosing on walk over
        break
    if h == 'H':                    #This mortar got hit, we lost the game
        alive = False
        display.show(Image.ASLEEP, wait=True, clear=False)
        break
    elif h == 'WO':
        break;

while True:         #Display result, Winner will still be alive when match is over.
    if alive:
        display.scroll("WINNER")
        display.show(Image.HAPPY)
    else:
        display.scroll("LOSER")
        display.show(Image.SAD)
    if button_a.is_pressed() and button_b.is_pressed():
        display.scroll("RESET")
        reset()
