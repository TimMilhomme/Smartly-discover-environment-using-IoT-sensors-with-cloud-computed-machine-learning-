import time
import sys
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread
import json
from json import encoder
import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser

class PILOTE:
    app = Flask(__name__)
    socketio = SocketIO(app)
    def __init__(self):
        #Innit Thymio
        os.system('ps -ef | grep asebamedulla | pkill -f asebamedulla ')
        os.system('asebamedulla "ser:device=/dev/ttyACM0" &')
        # Flask+SocketIO boilerplate code
        
        # Initialize a global thread object
        self.thread = None
        self.on = False

        self.joystickX = 0
        self.joystickY = 0
      
            
    def controlThymio(self):
        
        global joystickX
        global joystickY
        
        speedX = self.joystickX*250
        speedY = self.joystickY*250
        
        self.moove(speedX,speedY)
        
    def background_controlThymio():
        global on
        global joystickX
        global joystickX
        
        while True:
            while on:
                self.controlThymio()
            while not on:
            #When stop is click make a pause
                time.sleep(0.003)
                speedX = 0
                speedY = 0
                self.moove(speedX,speedY)
                
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

    # When a client sends a request, get the LIDAR data
    @app.route('/')
    def index():
      global thread
      global joystickX
      global joystickY
      
      # Start the getData() thread when the client makes the first request
      while thread is None:

            thread = Thread(target=background_controlThymio)
            thread.start()
            
      return render_template('index.html')

    @socketio.on('my event')
    def my_event(msg):
      print (msg['data'])    
    @socketio.on('connect')
    def on_connect():
      emit('rsp',{'status':'CONNECTED'})
    @socketio.on('disconnect')
    def on_connect():
      print ('Client disconnected!')

    @socketio.on('state button')
    def button_state(msg):
      global on

      if msg['data'] == 'Exit':  
        sys.exit()
      if msg['data'] == 'joystickActivation':
        on = True
      if msg['data'] == 'joystickDesctivation':
        on = False

    @socketio.on('joystickValue')
    def joystick_value(msg):
        global joystickX
        global joystickY
        
        _joystick = json.dumps(msg)
        joystick = json.loads(_joystick)
        joystickX = float(joystick['x'])
        joystickY = float(joystick['y'])
    
    
    def runPilote(self):
        
        socketio.run(app, host='0.0.0.0')
