#!/usr/bin/env python
import math
import csv
import time
import numpy as np
import PyLidar3
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import matplotlib.pyplot as plt

class HARVEST:
    #Initialise sensors
    def __init__(self):
        #Initialise LIDAR
        self.port = '/dev/ttyUSB0'
        self.lidar = PyLidar3.YdLidarX4(self.port)
        if(self.lidar.Connect()):
            print (self.lidar.GetDeviceInfo())
        #Initialise IMU   
        self.mpu = MPU9250(
            address_ak=AK8963_ADDRESS, 
            address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
            address_mpu_slave=None, 
            bus=1,
            gfs=GFS_1000, 
            afs=AFS_8G, 
            mfs=AK8963_BIT_16, 
            mode=AK8963_MODE_C100HZ)
        self.mpu.configure() # Apply the settings to the registers.
        
        with open('IMUData.csv','w',newline='') as self.IMUData:
            self.writerIMU = csv.DictWriter(self.IMUData, delimiter = ',',fieldnames = ['field.header.stamp',
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
            self.writerIMU.writeheader()
        
        with open('LidarData.csv','w',newline='') as self.LidarData:
            fieldnames = ['field.header.stamp']

            for i in range(360):
                fieldnumber = 'field.ranges' + str(i) 
                fieldnames +=  [fieldnumber]
                
            self.writerLIDAR = csv.writer(self.LidarData, delimiter = ',')    
            self.writerLIDAR.writerows(fieldnames)                
    #Harvest data of lidar in a dictionary
    def getDataLidar(self):

        self.gen = self.lidar.StartScanning()
        data = dict(next(self.gen))
        for angle in range(0,360):
            self.x[angle] = data[angle] * math.cos(math.radians(angle))
            self.y[angle] = -data[angle] * math.sin(math.radians(angle))
        self.lidar.StopScanning()
        return data       
    #Harvest and save IMU data in a csv file         
    def IMUHarvest(self):          
            
        with open('IMUData.csv','w',newline='') as self.IMUData:
            timeNow = time.time()
            magne_data = self.mpu.readMagnetometerMaster()
            gyro_data = self.mpu.readGyroscopeMaster()
            accel_data = self.mpu.readAccelerometerMaster()
            self.writerIMU.writerows({'field.header.stamp':timeNow,
                              'field.orientation.x':magne_data[0],
                              'field.orientation.y':magne_data[1],
                              'field.orientation.z':magne_data[2],
                              'field.orientation.w':1, 
                              'field.angular_velocity.x':gyro_data[0],
                              'field.angular_velocity.y':gyro_data[1],
                              'field.angular_velocity.z':gyro_data[2],
                              'field.linear_acceleration.x':accel_data[0],
                              'field.linear_acceleration.y':accel_data[1],
                              'field.linear_acceleration.z':accel_data[2] })
    
    #Save LIDAR data in csv file
    def LIDARHarvest(self):
        with open('LidarData.csv','w',newline='') as self.LidarData:
            self.x=[]
            self.y=[]
            for _ in range(360):
                self.x.append(0)
                self.y.append(0)
            lidar_data = self.getDataLidar()
            timeNow = time.time()
            row=[timeNow]
            for key in lidar_data.keys():
                row.append(lidar_data[key])
            self.writerLIDAR.writerows(row)

