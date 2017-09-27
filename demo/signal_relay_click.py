
#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

relay = [4,5,8,18]
relay2 = [13,12,7,17]

def init_relay(number_bus):
   global relay
   global relay2
   if(number_bus == 1):
        for i in range(0,4):
           set = relay[i]
           GPIO.setup(set, GPIO.OUT)
   else:
        for i in range(0,4):
           set = relay2[i]
           GPIO.setup(set, GPIO.OUT)

def relay_on(number_bus, number_relay):
   global relay
   global relay2
   if( number_bus == 1 ):
        out = relay[number_relay]
        GPIO.output(out,GPIO.HIGH)
   else:
        out = relay2[number_relay]
        GPIO.output(out,GPIO.HIGH)

def relay_off(number_bus, number_relay):
   global relay
   global relay2
   if( number_bus == 1 ):
        out = relay[number_relay]
        GPIO.output(out,GPIO.LOW)
   else:
        out = relay2[number_relay]
        GPIO.output(out,GPIO.LOW)

init_relay(1)
while True:
        print "On!"
        for i in range(0,4):
                relay_on(1,i)
                sleep(1)
        sleep(2)
        print "Off"
        for i in range(0,4):
                relay_off(1,i)
                sleep(1)
        sleep(2)

GPIO.cleanup()
