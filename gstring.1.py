#!/usr/bin/python
#written by Aneesh PA, on 21 Dec 2014
#reads gps data from serial interface, rapi's gpio and
#pushes relevant fields into a string, 

import serial
import time
from pynmea import nmea
#import subprocess
import socket

serial_port="/dev/ttyAMA0"
baudrate=9600
#host changed from 231 to 230
#HOST="10.151.6.3"
#PORT=6870
HOST="127.0.0.1"
PORT=53005

def get_gps_string():
    '''Writes latest gps string to the file'''
    appId = "A"         #A = GPS tracker
    messageId = "A"     # A = GPS data, B = storing GPS data
    Imei = "355435047096119"    #IMEI 15 chars
    GpsFix ="B"     #A=DataValid,B=invalid,X=GPSnotworkin,M = Masked
    GpsTime = "000000"  #hhmmss, use GPRMC
    GpsDate = "000000"  #ddmmyy, use GPRMC
    Lati = "0000.0000"  #ddmm.mmmm, use GGA
    NorthSouth = "0"    #N or S, use GGA
    Longi = "00000.0000" #ddmm.mmmm, use GGA
    EastWest = "0"      #E or W, use GGA
    Sog = "000000"      #speed over ground, use GPVTG
    Cog = "000000"      #course over ground, use GPVTG
    Sats = "00"       #no of satellites, use GPGGA
    Hdop = "0000"     #Horizontal dilution of precision, use GPGGA
    StrengthQual = "0000"   #signal strength and qual. of gprs
    PowerMode = "0"      #
    BatLevel = "000"
    AiVal = "0000"
    AiVal2 = "0000"
    DailyDist = ""
    OdoDist = ""
    DiStat = "0000"
    CrLf = '\n'+'\t'
    gpgga = nmea.GPGGA()
    #gpgll = nmea.GPGLL()
    #gpvtg = nmea.GPVTG()
    gprmc = nmea.GPRMC()
    ser = serial.Serial(serial_port, baudrate, timeout=0.1)
    #data='0000'
    for i in range(10):
	#print "::i::" + str(i)
	try:
            data = ser.readline()
            #print "::data::" + data + "\n"
        except serial.serialutil.SerialException, e:
	    print "serial exception raised"+error(e)
	    sleep(2)
	    pass
	#finally:
	    #ser.close()
	if data.startswith('$GPGGA'):
            gpgga.parse(data)			#ref nmea
            Sats = gpgga.num_sats
            Hdop = gpgga.horizontal_dil
	elif data.startswith('$GPRMC'):
            gprmc.parse(data)
            GpsDate = gprmc.datestamp
            GpsTime = gprmc.timestamp
            GpsFix = gprmc.data_validity
            Lati = gprmc.lat
            Longi = gprmc.lon
            Sog = gprmc.spd_over_grnd
            Cog = gprmc.true_course
            NorthSouth = gprmc.lat_dir
            EastWest = gprmc.lon_dir
    msgString ='$'+appId+'#'+messageId+'#'+Imei+'#'+GpsFix+'#'+GpsTime[:6]+'#'+\
      	GpsDate+'#'+Lati[:9]+'#'+NorthSouth+'#'+Longi[:10]+'#'+EastWest+'#'+\
      	Sog+'#'+Cog+'#'+Sats+'#'+Hdop+'#'+ StrengthQual+'#'+PowerMode+'#'+\
      	BatLevel+'#'+AiVal+'#'+AiVal2+'#'+DiStat+'*'+CrLf
    ser.close()
    #print "message is: " + msgString 
    logFile='/media/pendrive/gps.log'
    fd=open(logFile, 'a')
    fd.write(msgString)
    fd.close()
    return msgString

def send_msg(g_msg):
    '''sends g_msg to remote server'''
    server_addr=(HOST,PORT)
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
       	sock.connect(server_addr)
	#print "sending msg" + g_msg
	sock.sendall(g_msg)
    except:
    	return
	print "error in sending"
    finally:
	sock.close() 
	#print "socket closed"

#about 40 strings per 6 minutes
#400*3 for 3 hours
if __name__== '__main__':
    for i in range(1200):
	print "reading from gps, count is:: "
	print i
        g_msg=get_gps_string()
	print "sending msg"+g_msg
	send_msg(g_msg)
	time.sleep(5)
