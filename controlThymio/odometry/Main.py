import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser

from odometry_thymio import *
odo = odometry_thymio()

running = False
flag = True
obstacle = False

forwardButton = [0]

maxTime = 30
travelled_dist = 200
obstacle_dist =300

startTime = time.time()

def get_button_forward_reply(r):
    global forwardButton
    forwardButton=r
def get_variables_error(e):
    print('error:')
    print(str(e))
    loop.quit()

# This function is executed over and over until the loop is quitted
# Its purpose is to allow the user to launch the robot whe desired
def startLoop():
    
    global startTime
    global running
    global flag
    
    # Fetching the state value of Thymio's forward button
    network.GetVariable("thymio-II", "button.forward",reply_handler=get_button_forward_reply,error_handler=get_variables_error)
    
    # Checking if the forward button is pressed to launch the main logic
    if flag:
        if forwardButton[0] == 1:
            running = True
            flag = False
            loop.quit()

    return True


# This part creates a loop that will run the startLoop function, and runs it every 0.01 sec
network = odo.connect_to_thymio()
loop = gobject.MainLoop()
handle = gobject.timeout_add(10, startLoop)
print('Press forward button')
loop.run()

startTime = time.time()

# This part is main navigation logic loop and is running only when the forward button as been pressed
while running:
#Create a SLAM lol
    
    # At each cycle the robot checks if its stopping condition is satisfied
    runTime = time.time()-startTime
    if runTime > maxTime:
        running = False

