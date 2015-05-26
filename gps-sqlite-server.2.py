#!/usr/bin/python
#author: aneesh
#written on 27March2015
import SocketServer
import os
import sqlite3
import time

dbfile='/var/www/gstring-sql.db'
#HOST="10.151.6.3"
HOST="127.0.0.1"
PORT=53005

class MyTCPHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    dbexist=os.path.exists(dbfile)
    db=sqlite3.connect(dbfile)
    cur=db.cursor()
    if not dbexist:
      sqlstring='CREATE TABLE gpsdata ( id INTEGER PRIMARY KEY, msgType TEXT, imei TEXT, validFix TEXT, \
gpsTime TEXT, gpsDate TEXT, lat TEXT, ns TEXT, lon TEXT, ew TEXT, sog TEXT, cog TEXT, sats TEXT, hdop TEXT)'
      cur.execute(sqlstring)
      db.commit()
    self.data=self.request.recv(100).strip()
    #print "{} wrote: ".format(self.client_address[0])
    print self.data
    gstring=self.data
    k=gstring.split("#")
    cur.execute("INSERT INTO gpsdata (id, msgType, imei, validFix, gpsTime, gpsDate, lat, ns, lon, ew, sog, cog, sats, hdop) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (None, k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9],k[10],k[11],k[12],k[13]))
    #cur.execute("INSERT INTO gpsdata (id, start, lat, lon) VALUES (?, ? ,?)", (None, gstring, "something"))
    db.commit()

if __name__=="__main__":
  server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
  server.serve_forever()
