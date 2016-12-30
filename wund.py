#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sqlite3 as lite
import requests
import sys

#wunderground logins
id="KORHILLS98"
password="password"

#enable (1) if using a BMP085 pressure sensor
BMP=1

######
## End of configurable values
######

if BMP=1: 
	import Adafruit_BMP.BMP085 as BMP085

#wind speed: 2 kph, wind direction: 225.0°, rain gauge: 0.00 in.
#wind speed: 2 kph, temp: 60.4° F, humidity: 70% RH

# CREATE TABLE wx(
# ID INT PRIMARY KEY,
# DT datetime default current_timestamp,
# TP TEXT,
# VL TEXT);

#connect to db
con = lite.connect('wx.db')
c = con.cursor()

def query(query): 
	c.execute(query)
	row = c.fetchall()
	temp = str(row[0][0])
	return temp

baro=""
if BMP=1: 
	try:
	    sensor = BMP085.BMP085()
	    baro='&baromin=' + sensor.read_pressure()*0.0002953
	except:
	    pass
	print baro
updates = int(query('select count(*) FROM wx where DT >= Datetime("now", "-10 minutes")'))
if updates < 10:
        #not enough data, don't post
	print 'BAD DATA. \nPossible connectivity issues.\n exiting...' + str(updates)
        sys.exit()

temp = query('SELECT VL FROM wx WHERE TP="TM" ORDER BY DT DESC LIMIT 1.')
print temp
wind = query('select AVG(VL) from wx where TP = "WS" and DT >= Datetime("now", "-10 minutes")')
wind2 = 0 if wind < 2 else wind
print 'wind:' + wind2


gust = query('select MAX(VL) from wx where TP = "WS" and DT >= Datetime("now", "-10 minutes")')
guststr= "&windgustmph=" + str(gust)

if (float(gust)-float(wind))<5.0:
	guststr=''

print gust

dir = query('select VL from WX where TP="WD" AND DT >= Datetime("now", "-10 minutes") GROUP BY VL ORDER BY COUNT(*) DESC LIMIT 1');
if wind < 1.0:
	dir = ''
print dir
hum = query('SELECT VL FROM wx WHERE TP="HM" ORDER BY DT DESC LIMIT 1.')
print hum
rain = query('SELECT VL FROM wx WHERE TP="RN" ORDER BY DT DESC LIMIT 1.')
print rain
rainrate = str(max(int(0), float(query('SELECT VL FROM wx WHERE TP="RN" ORDER BY DT DESC LIMIT 1;')) - float(query('SELECT VL FROM wx WHERE TP="RN" AND DT >= Datetime("now", "-10 minutes") ORDER BY DT ASC LIMIT 1;')))*6)
print rainrate
dew = str(float(temp) - ((100 - float(hum))/5))
print dew
windchill = 35.74 + (0.6215*float(temp)) - 35.75*(float(wind)**0.16) + 0.4275*float(temp)*(float(wind)**0.16)
print windchill

url='https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID={}&PASSWORD={}&dateutc=new&winddir={}&windspeedmph={}{}&tempf={}&rainin={}&dailyrainin={}&humidity={}&dewptf={}{}&softwaretype=custom%20uploader&action=updateraw'.format(id,password,dir,wind,guststr,temp,rainrate,rain,hum,dew,baro)
#print url
r = requests.get(url)
print r.status_code
