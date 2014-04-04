#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import spidev
 
GPIO.setmode(GPIO.BCM)
DEBUG = 1

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
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        #if ((adcnum > 1) or (adcnum < 0)):
        #        return 0
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
 
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
 
# Vibration Sensor #1 attached to #adc0, Sensor #2 attached to adc#1
team_1 = 0;
team_2 = 1;
 
#last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

try:
            
     while True:
     # we'll assume that the pot didn't move
     #trim_pot_changed = False
    
     
         # read the analog pin
         #team_1_read = readadc(team_1, SPICLK, SPIMOSI, SPIMISO, SPICS)
         #team_2_read = readadc(team_2, SPICLK, SPIMOSI, SPIMISO, SPICS)
         team_1_read = get_adc(team_1);
         team_2_read = get_adc(team_2);
         
         # how much has it changed since the last read?
         #pot_adjust = abs(trim_pot - last_read)
    
         #if DEBUG:
         print "team_1_read:", team_1_read
         print "team_2_read:", team_2_read
    
     #if ( team_1_read > tolerance ):
     #       trim_pot_changed = True
    
     #if DEBUG:
     #        print "trim_pot_changed", trim_pot_changed
    
     #if ( trim_pot_changed ):
     #set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
     #set_volume = round(set_volume)          # round out decimal value
     #set_volume = int(set_volume)            # cast volume as integer
    
     #print 'Volume = {volume}%' .format(volume = set_volume)
     #set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
     #os.system(set_vol_cmd)  # set volume
    
     #if DEBUG:
     #       print "set_volume", set_volume
     #       print "tri_pot_changed", set_volume
    
    # save the potentiometer reading for the next loop
     #last_read = trim_pot
    
     # hang out and do nothing for a half second
         time.sleep(0.5)
except:
    print "Exception occured";
finally:
    GPIO.cleanup()