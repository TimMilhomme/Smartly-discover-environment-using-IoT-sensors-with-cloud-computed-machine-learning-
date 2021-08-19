#!/usr/bin/python
'''
Flask-powered web app for visualizing
YDLIDAR X4 data and controlling Thymio
'''
# Make the standard library 'play nicely'
from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Get the LIDAR data
import PyLidar3
import json
from json import encoder

# Run the getData() function in the background
from threading import Thread
import time
import sys
import os

# Libraries for Thymio
import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser
from odometry_thymio import *
odometry = odometry_thymio()

# Flask+SocketIO boilerplate code
app = Flask(__name__)
socketio = SocketIO(app)
# Initialize a global thread object
thread = None
thread2 = None
on = False
on2 = False
_data = dict()

joystickX = 0
joystickY = 0

# Configure the LIDAR interface
port = '/dev/ttyUSB0'
lidar = PyLidar3.YdLidarX4(port)
if(lidar.Connect()):
  print (lidar.GetDeviceInfo())
  
#Configure Thymio
os.system('ps -ef | grep asebamedulla | pkill -f asebamedulla ')
os.system('asebamedulla "ser:device=/dev/ttyACM0" &')
  
# Function for actually getting the lidar data
def getData():
  global _data
  gen = lidar.StartScanning()
  data = dict(next(gen))
  lidar.StopScanning()
  _data = json.dumps(data)

# Run the getData() function continuously in the background to update _data object!
def background_getData():
  global _data
  global on
  # Run continuously!
  while True:
      while on:
        # Send how fast we're getting data from the device
        t0 = time.time()
        getData()
        t = time.time()-t0
        # Send the data in a websocket event, which I'll call 'message'
        socketio.emit('message', {'data':_data,'time':'%.3f'%t})
      while not on:
        #When stop is click make a pause
        time.sleep(0.1)
        
def controlThymio():
    
    global joystickX
    global joystickY
    
    speedX = joystickX*500
    speedY = joystickY*500
    
    odometry.moove(speedX,speedY)
    
def background_controlThymio():
    global on2
    global joystickX
    global joystickX
    
    while True:
        while on2:
            controlThymio()
        while not on2:
        #When stop is click make a pause
            time.sleep(0.1)
            
# When a client sends a request, get the LIDAR data
@app.route('/')
def index():
  global thread
  global theard2
  global joystickX
  global joystickY
  
  # Start the getData() thread when the client makes the first request
  while thread is None:
        thread = Thread(target=background_getData)
        thread2 = Thread(target=background_controlThymio)
        thread.start()
        thread2.start()
        
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
  global on2
  
  if msg['data'] == 'Start':
    on = True
  if msg['data'] == 'Stop':
    on = False
  if msg['data'] == 'Exit':  
    sys.exit()
  if msg['data'] == 'joystickActivation':
    on2 = True
  if msg['data'] == 'joystickDesctivation':
    on2 = False

@socketio.on('joystickValue')
def joystick_value(msg):
    global joystickX
    global joystickY
    
    _joystick = json.dumps(msg)
    joystick = json.loads(_joystick)
    joystickX = float(joystick['x'])
    joystickY = float(joystick['y'])

if __name__ == '__main__':
    
    socketio.run(app, host='0.0.0.0')
