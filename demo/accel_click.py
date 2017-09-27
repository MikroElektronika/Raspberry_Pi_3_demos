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
