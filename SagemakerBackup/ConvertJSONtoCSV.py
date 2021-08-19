import pandas as pd
import csv
from datetime import datetime


pdObj = pd.read_json('DeliveryLidarJSON.json', lines=True).to_dict(orient='dict')
lidar_file=open('DeliveryLidarCSV.csv','w',newline='')
fieldnames = ['field.header.stamp']

for i in range(360):
    fieldnumber = 'field.ranges'+str(i)
    fieldnames += [fieldnumber]

write=csv.writer(lidar_file)
write.writerow(fieldnames)

for key in pdObj['field.header.stamp']:
    row=[]
    row.append(int(pdObj['field.header.stamp'][key]))
    
    for i in range(0,360):
        row.append(pdObj['field.ranges'+str(i)][key])
    write.writerow(row)

lidar_file.close()

IMUJson = pd.read_json('DeliveryIMUJSON.json', lines=True).to_dict(orient='dict')
IMU_file=open('DeliveryIMUCSV.csv','w',newline='')


writerIMU = csv.DictWriter(IMU_file,fieldnames = ['field.header.stamp',
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
for key in IMUJson['timestamp']:
    writerIMU.writerow({'field.header.stamp':int(datetime.timestamp(IMUJson["timestamp"][key])),
                    'field.orientation.x':IMUJson["MagnetometerX"][key],
                    'field.orientation.y':IMUJson["MagnetometerY"][key],
                    'field.orientation.z':IMUJson["MagnetometerY"][key],
                    'field.orientation.w':1, 
                    'field.angular_velocity.x':IMUJson["GyroscopeX"][key],
                    'field.angular_velocity.y':IMUJson["GyroscopeX"][key],
                    'field.angular_velocity.z':IMUJson["GyroscopeX"][key],
                    'field.linear_acceleration.x':IMUJson["AccelereometerX"][key],
                    'field.linear_acceleration.y':IMUJson["AccelereometerX"][key],
                    'field.linear_acceleration.z':IMUJson["AccelereometerX"][key] })

IMU_file.close()