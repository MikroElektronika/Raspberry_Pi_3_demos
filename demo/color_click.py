import smbus
import time

i2c = smbus.SMBus(1)
device_address = 0x53

DATA_FORMAT = 0x31
BW_RATE     = 0x2C
FIFO_CTL    = 0x38
POWER_CTL   = 0x2D
ACCEL_ERROR = 0x02

reading = [ 0, 0, 0 ]
def write_data( address_reg, data ):
    global device_address
    i2c.write_byte_data(device_address, address_reg, data)

def init_accel():
   global device_address
   global DATA_FORMAT
   global BW_RATE
   global FIFO_CTL
   global ACCEL_ERROR

   id = 0x00
   write_data( ACCEL_ERROR, 0x00 )
   id = i2c.read_byte_data(device_address, 0x00)
   print id
   if ( id != 0xE5 ):
       return ACCEL_ERROR
   else:
       write_data( DATA_FORMAT, 0x08 )
       write_data( BW_RATE, 0x0A )
       write_data( FIFO_CTL, 0x80 )
       write_data( POWER_CTL, 0x08 )
       return 0x00

def accel_read( H_reg, L_reg ):
   global device_address
   H_out = i2c.read_byte_data(device_address,H_reg)
   L_out = i2c.read_byte_data(device_address,L_reg)
   H_out = ( H_out << 8 )
   H_out = ( H_out | L_out )
   return H_out

def accel_average():
   global reading
   sx = 0
   sy = 0
   sz = 0
   for i in range(0,15):
       sx = sx + accel_read( 0x33, 0x32 ) # X (high_reg, low_reg)
       sy = sy + accel_read( 0x35, 0x34 ) # Y (high_reg, low_reg)
       sz = sz + accel_read( 0x37, 0x36 ) # Z (high_reg, low_reg)
   reading[0] = sx >> 4
   reading[1] = sy >> 4
   reading[2] = sz >> 4

def display_value():
   global reading

   print reading[0]
   print reading[1]
   print reading[2]
   print "       "
   reading = [0,0,0]
if( init_accel() == 0 ):
    print "Initialize Acceleromerer"
else:
   print "Error!!! "

while True:

   accel_average()
   display_value()
   time.sleep(3)
pi@raspberrypi:~/click $ ls
accel_i2c.py                   adafruit_uart.py  lora_2.py         lora.py       lora_test.py  matrix_8x8_spi.py       matrix_8x8_spi.pyu  signal_relay_gpio.py  two_relay_gpio.py  uart.py.save      weather_i2c.py
adafruit-beaglebone-io-python  color_i2c.py      lora_adafruit.py  lora.py.save  l.py          matrix_8x8_spi.py.save  read.py             temp_hum_i2c.py       uart.py            weather_click.py
pi@raspberrypi:~/click $ sudo nano ^C
pi@raspberrypi:~/click $ sudo nano color_i2c.py
pi@raspberrypi:~/click $ sudo python color_i2c.py
Traceback (most recent call last):
  File "color_i2c.py", line 81, in <module>
    init_color()
  File "color_i2c.py", line 17, in init_color
    write_data( 0x80, 0x1B ) # color init
  File "color_i2c.py", line 14, in write_data
    i2c.write_byte_data(device_address, address_reg, data)
IOError: [Errno 121] Remote I/O error
pi@raspberrypi:~/click $ sudo python color_i2c.py
 RED : 15
 GREEN : 9
 BLUE : 5

 RED : 16
 GREEN : 60
 BLUE : 17

^X RED : 48
 GREEN : 31
 BLUE : 18

^Z
[4]+  Stopped                 sudo python color_i2c.py
pi@raspberrypi:~/click $ cat color_i2c.py

import smbus
import time

i2c = smbus.SMBus(1)
device_address = 0x29

sum_red = 0
sum_blue = 0
sum_green = 0

def write_data( address_reg , data ):
   global  device_address
   i2c.write_byte_data(device_address, address_reg, data)

def init_color():
    write_data( 0x80, 0x1B ) # color init
    write_data( 0x8f, 0x10 ) # configurate
    write_data( 0x81, 0x00 ) # RGBC ADC time

def color_read( L_address_reg, H_address_reg ):
    global device_address
    low_data  = i2c.read_byte_data( device_address, L_address_reg )
    high_data = i2c.read_byte_data( device_address, H_address_reg )
    high_data = ( high_data << 8 )
    color_data =  ( high_data | low_data )
    return color_data

def color_RGB():
    global  sum_red
    global  sum_green
    global  sum_blue
    for i in range(0,15):
         clear = color_read( 0x94, 0x95 )
         time.sleep(0.02)
         red = color_read ( 0x96, 0x97)
         green = color_read( 0x98, 0x99 )
         blue =  color_read( 0x9A, 0x9B )

         sum_red  = sum_red + (float(red)/ 100.0)
         sum_green = sum_green + (float(green)/100.0)
         sum_blue = sum_blue + (float(blue)/ 100.0)
         time.sleep( 0.04 )

    sum_red = sum_red / 16.0
    sum_green = sum_green / 16.0
    sum_blue = sum_blue / 16.0

    print " RED :" , int(sum_red)
    print " GREEN :" ,  int(sum_green)
    print  " BLUE :" , int(sum_blue)
    print "             "

def max_value(a,b):
   return a if a>b else b

def min_value(a,b):
   return a if a<b else b

def rgb_min_max(red,green,blue):
   fmax = max_value(max_value(red,green),blue)
   fmin = min_value(min_value(red,green),blue)
   if(fmax > 0):
      s = (fmax - fmin)/fmax
   else:
      s = 0
   if (s == 0):
      value = 0
   else:
      if(fmax == red):
          value = (green - blue) / (fmax - fmin)
      elif(fmax == green):
          value = 2 + (blue - red) / (fmax - fmin)
      else:
          value = 4 + (red - green) / (fmax - fmin)
      value = value / 6
      if (value < 0):
          value = value + 1
   return value

init_color()

while True:
     color_RGB()
     time.sleep(3)
