#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sqlite3 as lite

#wind speed: 2 kph, wind direction: 225.0°, rain gauge: 0.00 in.
#wind speed: 2 kph, temp: 60.4° F, humidity: 70% RH

def insert(type, val):
		con = lite.connect('/home/pi/wx.db')
		cur = con.cursor()
		cur.execute("INSERT INTO wx (TP, VL) VALUES ('%s', '%s')" % (type, val))
		con.commit()
		con.close()
p = subprocess.Popen("/usr/local/bin/rtl_433 -R 9", shell=True, stdout=subprocess.PIPE, bufsize=1)
for line in iter(p.stdout.readline, b''):
		print ":" + line,
		line = line.replace('°', '')
		windstr= "wind speed: "
		if line.find(windstr) > -1:
			#print "a",
			wind=str(int(line[line.find(windstr)+len(windstr):line.find("kph",line.find(windstr))])).strip()
			print str(wind)
			insert("WS", str(wind))
		
		winddir="wind direction: "
		if line.find(winddir) > -1:
			#print "a",
			dir=str(line[line.find(winddir)+len(winddir):line.find(",",line.find(winddir))]).strip()
			print str(dir)
			insert("WD", str(dir))		
		
		rainstr= "rain gauge: "
		if line.find(rainstr) > -1:
			#print "a",
			rain=str(line[line.find(rainstr)+len(rainstr):line.find("in.",line.find(rainstr))]).strip()
			print str(rain)
			insert("RN", str(rain))		
				
		tempstr= "temp: "
		if line.find(tempstr) > -1:
			#print "a",
			temp=str(line[line.find(tempstr)+len(tempstr):line.find(" F",line.find(tempstr))]).strip()
			print str(temp)
			insert("TM", str(temp))			
		
		humstr= "humidity: "
		if line.find(humstr) > -1:
			#print "a",
			hum=str(line[line.find(humstr)+len(humstr):line.find("%",line.find(humstr))]).strip()
			print str(hum)
			insert("HM", str(hum))			
p.stdout.close()
p.wait()

