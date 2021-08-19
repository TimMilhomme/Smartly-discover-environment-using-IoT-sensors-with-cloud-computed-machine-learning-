#!/usr/bin/env python
import numpy as np
import PyLidar3
import math
import csv
import matplotlib.pyplot as plt
from mpu6050 import mpu6050
import time

mpu = mpu6050(0x68)
port = '/dev/ttyUSB0'
lidar = PyLidar3.YdLidarX4(port)

def getData():
    global data
    global lidar
    global x
    global y
    gen = lidar.StartScanning()
    data = dict(next(gen))
    for angle in range(0,360):
        x[angle] = data[angle] * math.cos(math.radians(angle))
        y[angle] = -data[angle] * math.sin(math.radians(angle))
    lidar.StopScanning()
    return data       

if(lidar.Connect()):
    print (lidar.GetDeviceInfo())
    x=[]
    y=[]
    for _ in range(360):
        x.append(0)
        y.append(0)

            
            
            
with open('IMUData.csv', 'w') as IMUData:
    writerIMU = csv.DictWriter(IMUData, delimiter = ',',fieldnames = ['field.header.stamp',
                                                                      'field.orientation.x',
                                                                      'field.orientation.y',
                                                                      'field.orientation.z',
                                                                      'field.orientation.w',
                                                                      'field.angular_velocity.x',
                                                                      'field.angular_velocity.y',
                                                                      'field.angular_velocity.z',
                                                                      'field.linear_acceleration.x',
                                                                      'field.linear_acceleration.y',
                                                                      'field.linear_acceleration.z'])
    writerIMU.writeheader()
    
    with open('LidarData.csv','w') as LidarData:
        fieldnames = ['field.header.stamp']
        for i in range(360):
            fieldnumber = 'field.ranges' + str(i) 
            fieldnames +=  [fieldnumber]   
        writerLIDAR = csv.writer(LidarData, delimiter = ',')
        writerLIDAR.writerow(fieldnames)
        
        for i in range(0,2):
            timeNow = time.time()
            gyro_data = mpu.get_gyro_data()
            accel_data = mpu.get_accel_data()
            writerIMU.writerow({'field.header.stamp':timeNow,
                              'field.orientation.x':0,
                              'field.orientation.y':0,
                              'field.orientation.z':0,
                              'field.orientation.w':0, 
                              'field.angular_velocity.x':gyro_data['x'],
                              'field.angular_velocity.y':gyro_data['y'],
                              'field.angular_velocity.z':gyro_data['z'],
                              'field.linear_acceleration.x':accel_data['x'],
                              'field.linear_acceleration.y':accel_data['y'],
                              'field.linear_acceleration.z':accel_data['z']})

            lidar_data = getData()
            row=[timeNow]
            for key in lidar_data.keys():
                row.append(lidar_data[key])
 
            writerLIDAR.writerow(row)

