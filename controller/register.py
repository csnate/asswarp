#!/usr/bin/env python
import serial
import time

port = serial.Serial()
port.baudrate = 9600
port.port = "/dev/ttyAMA0"
port.timeout = 0.1
port.open()

cards = [
         '0C003375F5BF',    # BLUE
]

if port.isOpen():
        print "Port is open: ", port.portstr

while True:
        port.flushInput()
        data = port.readline().strip()
        if len(data) > 0:
                rfidData = data[1:13]
                print "Card scanned: ", rfidData
                
