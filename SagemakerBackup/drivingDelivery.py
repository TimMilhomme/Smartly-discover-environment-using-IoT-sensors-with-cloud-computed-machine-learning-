import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import time as t
import json
import PyLidar3
import math
from RandomPilote import RANDOMPILOTE
import random
import os
import sys

#Initialize IMU
mpu = MPU9250(
            address_ak=AK8963_ADDRESS, 
            address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
            address_mpu_slave=None, 
            bus=1,
            gfs=GFS_1000, 
            afs=AFS_8G, 
            mfs=AK8963_BIT_16, 
            mode=AK8963_MODE_C100HZ)
mpu.configure() # Apply the settings to the registers.

#Initilise Lidar
port = '/dev/ttyUSB0'
lidar = PyLidar3.YdLidarX4(port)
if(lidar.Connect()):
    print (lidar.GetDeviceInfo())

#Innit Thymio
os.system('ps -ef | grep asebamedulla | pkill -f asebamedulla ')
os.system('asebamedulla "ser:device=/dev/ttyACM0" &')

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "ac6s09xm1v6hb-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "Lidar"
PATH_TO_CERT = "/home/pi/Desktop/ProjetATRL/IoTCore/certsLidar/1d5833040b-certificate.pem.crt"
PATH_TO_KEY = "/home/pi/Desktop/ProjetATRL/IoTCore/certsLidar/1d5833040b-private.pem.key"
PATH_TO_ROOT = "/home/pi/Desktop/ProjetATRL/IoTCore/certs/AmazonRootCA1.pem"
TOPIC = "Lidar/result"


myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

    
randompilote = RANDOMPILOTE()

def getDataLidar():
    x=[]
    y=[]
    for _ in range(360):
        x.append(0)
        y.append(0)
    gen = lidar.StartScanning()
    data = dict(next(gen))
    for angle in range(0,360):
        x[angle] = data[angle] * math.cos(math.radians(angle))
        y[angle] = -data[angle] * math.sin(math.radians(angle))
    lidar.StopScanning()
    return data

def harvestIMU():
    
    myAWSIoTMQTTClient.connect()
    
    timeNow = t.time()
    magne_data = mpu.readMagnetometerMaster()
    gyro_data = mpu.readGyroscopeMaster()
    accel_data = mpu.readAccelerometerMaster()

    MagX = magne_data[0]
    MagY = magne_data[1]
    MagZ = magne_data[2]
    MagW = 1
    GyroX = gyro_data[0]
    GyroY = gyro_data[1]
    GyroZ = gyro_data[2]
    AccX = accel_data[0]
    AccY = accel_data[1]
    AccZ = accel_data[2]
    
    message = {'timestamp':timeNow,
               'MagnetometerX':MagX,
               'MagnetometerY':MagY,
               'MagnetometerZ':MagZ,
               'MagnetometerW':MagW,
               'GyroscopeX':GyroX,
               'GyroscopeY':GyroY,
               'GyroscopeZ':GyroZ,
               'AccelereometerX':AccX,
               'AccelereometerY':AccY,
               'AccelereometerZ':AccZ}
    
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'Lidar/result'")
    myAWSIoTMQTTClient.disconnect()
    
def harvestLidar():
    
    myAWSIoTMQTTClient.connect()
    
    timeNow = t.time()
    lidar_data = getDataLidar()
    
    message = {'timestamp':timeNow,'LidarData':lidar_data}
    
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'Lidar/result'")
    myAWSIoTMQTTClient.disconnect()
    

#Do  steps with one  one random orientation and one 20cm moove forward
for x in range(4):
    
    #Get Lidar values
    harvestLidar()
    #Turn randomly
    t0 = t.time()
    theta = random.uniform(0, 3.365)
    t1 = 0
    #Turn random
    while t1 < theta:
        t1 = t.time()-t0
        randompilote.moove(250,-250)
        #Get IMU values
        harvestIMU()
        print('Turn')

    #Moove 20cm forward
    t2 = t.time()
    delta = 2.35
    t3 = 0
    while t3 < delta:
        t3 = t.time()-t2
        randompilote.moove(250,250)
        harvestIMU()
        print('MoveForward')
        
    randompilote.moove(0,0)

    



