#!/usr/bin/python
import sys, os
import time
import serial
import numpy as np
import json

# serial port to connect to
device = '/dev/ttyUSB0'
speed = 115200
serialObj = None

# initialization
num_data = 2
data = np.ones(num_data) # data[0] = temperature, data[1] = humidity
str_data = ['0', '0']
timestamp_last_data = 0;
REC_PRD = 1 * 30 # seconds

f_temp = open('weather_log.json', 'r')
if f_temp.read() == '':
    table = [];
else:
    f_temp.close()
    f_temp = open('weather_log.json', 'r')
    table = json.load(f_temp)

    fp = open('weather_log_' + str(time.time()) + '.json', 'w')
    json.dump(table, fp)
    fp.close()
f_temp.close()

# ------ MAIN ------

if __name__ == '__main__':

    # grab port from command line
    if(len(sys.argv) != 1 and len(sys.argv) != 3):
        print "\nUsage: \n\trec_temphum.py [-p device]\n"
        sys.exit()

    if len(sys.argv) == 3:
        if sys.argv[1] == "-p":
            device = sys.argv[2]
        else:
            print "\nUsage: \n\trec_temphum.py [-p device]\n"
            sys.exit()

    print "\nTrying to connect to device " + device + " ..."

    # exit strategy, ensuring that the process is killed upon exit
    def handle_close(evt):
        f_temp = open('weather_log.json', 'w')
        table = json.dump(table, f_temp)
        f_temp.close()

        fp = open('weather_log_' + str(time.time()) + '.json', 'w')
        json.dump(table, fp)
        fp.close()

        sys.exit()

    serialObj = serial.Serial(device, speed, timeout=0.5)
    if not serialObj:
        print '\nError: could not open device!'
        sys.exit(1)
    else:
        print 'Successfully connected to device!\n'

    found_temp = False
    found_hum = False

    while 1:

        timestamp_current = time.time()
        if timestamp_current - timestamp_last_data < REC_PRD:
            time.sleep(REC_PRD/5.0)
        else:
            timestamp_last_data = timestamp_current
            serialObj.flushInput();
            found_temp = False
            found_hum = False
            while(not found_temp or not found_hum):
                
                buf = serialObj.readline()
                if len(buf) < 1:
                    # time.sleep(10/1000)
                    continue
                
                if buf[0:11] == 'Temperature' and len(buf) == 17:
                    data[0] = int(buf[13:15])
                    str_data[0] = buf[13:15]
                    found_temp = True
                elif buf[0:8] == 'Humidity' and len(buf) == 21:
                    data[1] = int(buf[13:15])
                    str_data[1] = buf[13:15]
                    found_hum = True

                serialObj.flush();

            print 'Temperature: ' + str_data[0]
            print 'Humidity:    ' + str_data[1] + '%'

            table.append({'time': timestamp_current, 'temperature': data[0], 'humidity': data[1]})
            f_temp = open('weather_log.json', 'w')
            json.dump(table, f_temp)
            f_temp.close()
