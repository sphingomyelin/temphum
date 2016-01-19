#!/usr/bin/python
import sys, os
import time
import serial
import numpy as np
import matplotlib as mpl
from matplotlib import cm
from matplotlib.pylab import subplots,close
import matplotlib.pyplot as plt
import json

mpl.rcParams['figure.subplot.bottom'] = 0.2
hour_ticks = 3

fp = open('weather_log.json', 'r')
table = json.load(fp)

x_values = np.zeros(len(table))
y_values_temp = np.zeros(len(table))
y_values_hum = np.zeros(len(table))
for i in range(0,len(table)):
	x_values[i] = table[i]['time']
	y_values_temp[i] = table[i]['temperature']
	y_values_hum[i] = table[i]['humidity']

# plot the data
# fig = plt.figure(1,(10,10))
fig = plt.figure(1)
# fig.autofmt_xdate(bottom=0.2,rotation=45,ha='left')

# set tick labels
tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst = time.localtime(table[0]['time'])
time_ticks_begin = time.mktime([tm_year,tm_mon,tm_mday,tm_hour,0,0,tm_wday,tm_yday,tm_isdst])
tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst = time.localtime(table[-1]['time'])
time_ticks_end   = time.mktime([tm_year,tm_mon,tm_mday,tm_hour,0,0,tm_wday,tm_yday,tm_isdst])
xticks_time = np.arange(time_ticks_begin + 60*60*hour_ticks, time_ticks_end + 60*60*hour_ticks, 60*60*hour_ticks)

xticks_label = list('')
time_new_day = list()
for i in range(0,len(xticks_time)):
	xticks_label.append('')	# do not have internet...
for i in range(0,len(xticks_time)):
	tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst = time.localtime(xticks_time[i])
	if tm_hour == 0:
		xticks_label[i] = '{0:2s}-{1:2s}-{2:2s}  {3:2s}h'.format(str(tm_year-2000).zfill(2),str(tm_mon).zfill(2),str(tm_mday).zfill(2),str(tm_hour).zfill(2))
		time_new_day.append(xticks_time[i])
	else:
		xticks_label[i] = '{0:2s}h'.format(str(tm_hour).zfill(2))

# Temperature
# plt.subplot(211)
ax = fig.add_subplot(111)
line_temp = ax.plot(x_values, y_values_temp, linewidth=1.0, color='r')
line_temp[0].set_label('Temperature')

[xmin, xmax, ymin, ymax] = ax.axis()
ax.axis([xmin, xmax, (ymin-2)-(ymin-2)%5, (ymax+5+2)-(ymax+5+2)%5])
# ax.plot(x_values, np.zeros(len(x_values)), linewidth=1.0, color='k')
# ax.plot([x_values[0], x_values[0]], [ymin, ymax], linewidth=1.0, color='k')
# ax.plot([], [], linewidth=1.0, color='m')[0]
# ax.axis([x_values[0], x_values[-1], 15, 35])
ax.grid('on', axis='x')
ax.grid('on', axis='y', which='both', markevery=1)
plt.xticks(xticks_time, xticks_label, rotation=45, ha='right')
plt.ticklabel_format(axis='x')
ax.set_ylabel('Temperature [degrees] (in red)')

plt.title('Temperature and Humidity vs Time')

# Humidity
ax2 = plt.twinx()
line_hum = ax2.plot(x_values, y_values_hum, linewidth=1.0, color='b')
line_hum[0].set_label('Humidity')

[xmin, xmax, ymin, ymax] = ax2.axis()
ax2.axis([xmin, xmax, (ymin-2)-(ymin-2)%5, (ymax+5+2)-(ymax+5+2)%5])
# ax2.plot(x_values, np.zeros(len(x_values)), linewidth=1.0, color='k')
# ax2.plot([x_values[0], x_values[0]], [ymin, ymax], linewidth=1.0, color='k')
# ax2.plot([], [], linewidth=1.0, color='m')[0]
# ax2.axis([x_values[0], x_values[-1], 20, 60])
# ax2.grid()
ax2.set_ylabel('Humidity [%RH] (in blue)')

# plt.legend( (line_temp, line_hum), ('Temperature', 'Humidity'), loc='best')

# ax.set_xlim(x_values[0], x_values[-1])
# ax.set_ylim(0, 50)
# ax.set_xticks(indices)
# ax.set_ylabel('Calibrated Distance (mm)',fontsize=14)
# ax.set_xlabel('Sensor Index',fontsize=14)


# Separate the days
for i in range(0,len(time_new_day)):
	ax2.plot([time_new_day[i], time_new_day[i]], [(ymin-2)-(ymin-2)%5, (ymax+5+2)-(ymax+2)%5], linewidth=2.0, color='k')


plt.show()
