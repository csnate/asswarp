#!/usr/bin/env python
import time
import sys
import os
import spidev
import ast
import urllib
import urllib2


# spidev setup
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
 
def send_goal(team):
    
    #data = "curl -X POST -H \"Content-Type: application/json\" -d '{\"type\": \"goal\",\"team\": \""
    #data = data + team
    #data = data + "\"}' http://10.60.3.155:8080/goal/"
    data = { "type": "goal", "team": team }
    url_data = urllib.urlencode(data)
    req = urllib2.Request(scoring_url, url_data)
    resp = urllib2.urlopen(req).read()
    lit_resp = ast.literal_eval(resp)
    score = int(lit_resp['score'])
    if score >= 5:
        time.sleep(10)
        register_teams()
    
def register_teams():
    data = "curl -X POST -H \"Content-Type: application/json\" -d '[{\"name\": \"black\",\"members\": [] }, {\"name\": \"yellow\",\"members\": [] }]' http://10.60.3.155:8080/teams/"
    os.system(data)
    
# Vibration Sensor #1 attached to #adc0, Sensor #2 attached to adc#1
team_1 = 0 # BLACK team
team_2 = 1 # YELLOW team
 
# tolerance levels
team_1_tolerance = 100
team_2_tolerance = 100

scoring_url = "http://10.60.3.155:8080/goal/"
register_url = "http://10.60.3.155:8080/teams/"

try:
     
     # Register the teams
     register_teams()
                 
     while True:

         # read the analog pin
         team_1_read = get_adc(team_1)
         team_2_read = get_adc(team_2)
    
         #if DEBUG:
         if team_1_read > team_1_tolerance:
             print "[DEBUG] TEAM 1: ", team_1_read
             send_goal("black")
             time.sleep(2)
             
         if team_2_read > team_2_tolerance:
             print "[DEBUG] TEAM 2: ", team_2_read
             send_goal("yellow")
             time.sleep(2)
    
         time.sleep(0.1)
except:
    print "Exception occurred - ", sys.exc_info()[0]
    
    
    
    