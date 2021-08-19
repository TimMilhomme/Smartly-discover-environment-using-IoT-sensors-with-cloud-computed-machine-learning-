import time
import sys
import os
import random
import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser


#Function connecting the Raspebbry Pi 4 to the Thymio II
def connect_to_thymio():
    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
    (options, args) = parser.parse_args()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    if options.system:
        bus = dbus.SystemBus()
    else:
        bus = dbus.SessionBus()
    #Create Aseba network
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
    
    return network

#Function making the robot moving forward with a dist input, wich is the ditance we want the robot to move in cm
def moove(motorLeft,motorRight):
    
    #Call the function connect to thymio
    network = connect_to_thymio()
    
    #send motor value to the robot
    network.SetVariable("thymio-II", "motor.left.target", [motorLeft])
    network.SetVariable("thymio-II", "motor.right.target", [motorRight])
    
    #Wait for the robot to move
    time.sleep(0.003) #seconds
    
    #Stop the robot
    totalRight = 0
    totalLeft = 0

    return True  

#Do 10 steps with one 10cm move and one random orientation
for x in range(0,10):

    #Turn rnadomly
    theta = random.randint(0, 359)
    while t < theta
        t = timeNow
        speedX = 250
        speedY = - 250
        moove(speedX,speedY)

    delta = 10

    #Moove 10cm
    while t < delta
        t = timeNow
        speedX = 250
        speedY = 250
        moove(speedX,speedY)
