#!/usr/bin/env python

import RPi.GPIO

GPIO.setmode(GPIO.BCM) 

button = 25
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def register_teams():
    data = "curl -X POST -H \"Content-Type: application/json\" -d '[{\"name\": \"black\",\"members\": [] }, {\"name\": \"yellow\",\"members\": [] }]' http://10.60.3.155:8080/teams/"
    os.system(data)

try:  
    GPIO.wait_for_edge(button, GPIO.FALLING)  
    register_teams()
    
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO o