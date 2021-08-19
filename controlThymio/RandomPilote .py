import time
import sys
import os
import random
import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser

class RANDOMPILOTE:
    def __init__(self):
        
        #Innit Thymio
        os.system('ps -ef | grep asebamedulla | pkill -f asebamedulla ')
        os.system('asebamedulla "ser:device=/dev/ttyACM0" &')
        
        
        
    #Function connecting the Raspebbry Pi 4 to the Thymio II
    def connect_to_thymio(self):
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
    def moove(self,motorLeft,motorRight):
        
        #Call the function connect to thymio
        network = connect_to_thymio(self)
        
        #send motor value to the robot
        network.SetVariable("thymio-II", "motor.left.target", [motorLeft])
        network.SetVariable("thymio-II", "motor.right.target", [motorRight])
        
        #Wait for the robot to move
        time.sleep(0.003) #seconds
        
        #Stop the robot
        totalRight = 0
        totalLeft = 0

        return True
