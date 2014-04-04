#!/usr/bin/env python
import time
#import RPi.GPIO as GPIO
import spidev
 
#GPIO.setmode(GPIO.BCM)
#DEBUG = 1

spi = spidev.SpiDev()
spi.open(0,0)
    
def get_adc(channel):
    # Only 2 channels 0 and 1 else return -1
    if ((channel > 1) or (channel < 0)):
            return -1
    
    # Send start bit, sgl/diff, odd/sign, MSBF
    # channel = 0 sends 0000 0001 1000 0000 0000 0000
    # channel = 1 sends 0000 0001 1100 0000 0000 0000
    # sgl/diff = 1; odd/sign = channel; MSBF = 0
    r = spi.xfer2([1,(2+channel)<<6,0])
    
    # spi.xfer2 returns same number of 8 bit bytes
    # as sent. In this case, 3 - 8 bit bytes are returned
    # We must then parse out the correct 10 bit byte from
    # the 24 bits returned. The following line discards
    # all bits but the 10 data bits from the center of
    # the last 2 bytes: XXXX XXXX - XXXX DDDD - DDDD DDXX
    ret = ((r[1]&31) << 6) + (r[2] >> 2)
    return ret
 

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
#SPICLK = 18
#SPIMISO = 23
#SPIMOSI = 24
#SPICS = 25
 
# set up the SPI interface pins
#GPIO.setup(SPIMOSI, GPIO.OUT)
#GPIO.setup(SPIMISO, GPIO.IN)
#GPIO.setup(SPICLK, GPIO.OUT)
#GPIO.setup(SPICS, GPIO.OUT)
 
# Vibration Sensor #1 attached to #adc0, Sensor #2 attached to adc#1
team_1 = 0
team_2 = 1
 
# tolerance levels
team_1_tolerance = 30
team_2_tolerance = 50

try:
            
     while True:

         # read the analog pin
         team_1_read = get_adc(team_1)
         team_2_read = get_adc(team_2)
    
         #if DEBUG:
         if team_1_read > team_1_tolerance:
             print "[DEBUG] TEAM 1: ", team_1_read
             
         if team_2_read > team_2_tolerance:
             print "[DEBUG] TEAM 2: ", team_2_read
    
         time.sleep(0.2)
except:
    print "Exception occurred"