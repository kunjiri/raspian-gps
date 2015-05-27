# raspian-gps
GPS based tracking using Raspberry Pi and ublox gps. 

gstring.py takes out gps string from ublox, and sends it to a tcp socket. Another python script reads it from the socket and then saves it into an sqlite database. Using javascript and php, a google map with latest gps location is generated. Raspberry runs lighttpd as web server.
