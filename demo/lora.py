
import time
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5,GPIO.HIGH)
time.sleep(1)
GPIO.output(5,GPIO.HIGH)

#reaset = ser.readln()
ser = serial.Serial(
               port = '/dev/serial0',
               baudrate = 57600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
           )

def readlineCR(ser):
    rv = ''
    while True:
        ch = ser.read()
        rv +=ch
        print ch
        if ch == '\n':
           return rv

def sendcmd( data ):
    ser.write(data)
    ser.write('\r\n')
    rcv = readlineCR(ser)
    time.sleep(3)
    print data,"........",rcv
    time.sleep(1)

reset = ser.readline()
sendcmd("sys reset")
time.sleep(0.5)
sendcmd("radio set mod lora")
time.sleep(0.5)
sendcmd("mac pause")
sendcmd("radio tx AF")
