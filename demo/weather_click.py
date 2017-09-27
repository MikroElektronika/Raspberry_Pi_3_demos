
import smbus
import time

i2c = smbus.SMBus(1)

device_address = 0x76
tmp_data = []

C_TMP = [ 0, 0, 0 ]
C_HUM = [ 0, 0, 0, 0, 0, 0 ]
C_PRE = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

HUMIDITY_DATA = 0
TEMPERATURE_DATA = 0
PRESSURE_DATA = 0
FINE = 0

BME280_PRESSURE     = 0xF7
BME280_ID           = 0xD0
BME280_RESET        = 0xB6
BME280_RST_REG      = 0xE0
BME280_STATUS       = 0xF3
BME280_MEAS_REG     = 0xF4
BME280_HUMIDITY_REG = 0xF2
BME280_CONFIG_REG   = 0xF5

BME280_TEMPERATURE_0_LSB_REG   = 0x88
BME280_TEMPERATURE_0_MSB_REG   = 0x89
BME280_TEMPERATURE_1_LSB_REG   = 0x8A
BME280_TEMPERATURE_1_MSB_REG   = 0x8B
BME280_TEMPERATURE_2_LSB_REG   = 0x8C
BME280_TEMPERATURE_2_MSB_REG   = 0x8D

BME280_PRESSURE_0_LSB_REG      = 0x8E
BME280_PRESSURE_0_MSB_REG      = 0x8F
BME280_PRESSURE_1_LSB_REG      = 0x90
BME280_PRESSURE_1_MSB_REG      = 0x91
BME280_PRESSURE_2_LSB_REG      = 0x92
BME280_PRESSURE_2_MSB_REG      = 0x93
BME280_PRESSURE_3_LSB_REG      = 0x94
BME280_PRESSURE_3_MSB_REG      = 0x95
BME280_PRESSURE_4_LSB_REG      = 0x96
BME280_PRESSURE_4_MSB_REG      = 0x97
BME280_PRESSURE_5_LSB_REG      = 0x98
BME280_PRESSURE_5_MSB_REG      = 0x99
BME280_PRESSURE_6_LSB_REG      = 0x9A
BME280_PRESSURE_6_MSB_REG      = 0x9B
BME280_PRESSURE_7_LSB_REG      = 0x9C
BME280_PRESSURE_7_MSB_REG      = 0x9D
BME280_PRESSURE_8_LSB_REG      = 0x9E
BME280_PRESSURE_8_MSB_REG      = 0x9F

BME280_HUMIDITY_0_CHR_REG      = 0xA1
BME280_HUMIDITY_1_LSB_REG      = 0xE1
BME280_HUMIDITY_1_MSB_REG      = 0xE2
BME280_HUMIDITY_2_CHR_REG      = 0xE3
BME280_HUMIDITY_3_MSB_REG      = 0xE4
BME280_HUMIDITY_3_LSB_REG      = 0xE5
BME280_HUMIDITY_4_MSB_REG      = 0xE6
BME280_HUMIDITY_5_CHR_REG      = 0xE7


def init_weather():

   id = BME280_get( BME280_ID )
   print "ID:  ", id
   if id != 0x60:
       print "ERROR..."
   else:
       print "INIT..."

def write_data( address_reg , data ):
    global device_address
    i2c.write_byte_data(device_address, address_reg, data)

def read_data(address_reg):
    global device_address
    tmp = i2c.read_byte_data(device_address,address_reg)
    return tmp

def BME280_read_Measurements():
    global device_address
    global BME280_PRESSURE
    global tmp_data
    global HUMIDITY_DATA,TEMPERATURE_DATA,PRESSURE_DATA

    tmp_data = i2c.read_i2c_block_data(device_address,BME280_PRESSURE) #size 8 byte
    # Humidity
    HUMIDITY_DATA  =  tmp_data[7]
    HUMIDITY_DATA |=  tmp_data[6]  << 8
    #Temperature
    TEMPERATURE_DATA = tmp_data[5] >> 4
    TEMPERATURE_DATA |= tmp_data[4] << 4
    TEMPERATURE_DATA |= tmp_data[3] << 12
    #Pressure
    PRESSURE_DATA = tmp_data[2] >> 4
    PRESSURE_DATA |= tmp_data[1] << 4
    PRESSURE_DATA |= tmp_data[0] << 12

def BME280_get(reg):
    return  read_data(reg)

def BME280_reset():
    global BME280_RST_REG
    global BME280_RESET
    write_data(BME280_RST_REG,BME280_RESET)

def read_LSB_MSB(msb_reg,lsb_reg):
    msb = read_data(msb_reg)
    lsb = read_data(lsb_reg)
    out = ( msb << 8 ) + lsb
    return out

def BME280_ReadCalibration():
   global C_TMP, C_PRE, C_HUM
   global BME280_TEMPERATURE_0_MSB_REG,BME280_TEMPERATURE_0_LSB_REG
   global BME280_TEMPERATURE_1_MSB_REG,BME280_TEMPERATURE_1_LSB_REG
   global BME280_TEMPERATURE_2_MSB_REG,BME280_TEMPERATURE_2_LSB_REG
   global BME280_PRESSURE_0_MSB_REG,BME280_PRESSURE_0_LSB_REG
   global BME280_PRESSURE_1_MSB_REG,BME280_PRESSURE_1_LSB_REG
   global BME280_PRESSURE_2_MSB_REG,BME280_PRESSURE_2_LSB_REG
   global BME280_PRESSURE_3_MSB_REG,BME280_PRESSURE_3_LSB_REG
   global BME280_PRESSURE_4_MSB_REG,BME280_PRESSURE_4_LSB_REG
   global BME280_PRESSURE_5_MSB_REG,BME280_PRESSURE_5_LSB_REG
   global BME280_PRESSURE_6_MSB_REG,BME280_PRESSURE_6_LSB_REG
   global BME280_PRESSURE_7_MSB_REG,BME280_PRESSURE_7_LSB_REG
   global BME280_PRESSURE_8_MSB_REG,BME280_PRESSURE_8_LSB_REG
   global BME280_HUMIDITY_0_CHR_REG,BME280_HUMIDITY_1_MSB_REG,BME280_HUMIDITY_1_LSB_REG
   global BME280_HUMIDITY_2_CHR_REG,BME280_HUMIDITY_3_MSB_REG,BME280_HUMIDITY_3_LSB_REG
   global BME280_HUMIDITY_4_MSB_REG,BME280_HUMIDITY_3_LSB_REG,BME280_HUMIDITY_5_CHR_REG

   C_TMP[0] = read_LSB_MSB(BME280_TEMPERATURE_0_MSB_REG, BME280_TEMPERATURE_0_LSB_REG )
   if(C_TMP[0] < 26000):
       C_TMP[0] = 28440
   C_TMP[1] = read_LSB_MSB(BME280_TEMPERATURE_1_MSB_REG, BME280_TEMPERATURE_1_LSB_REG )
   C_TMP[2] = read_LSB_MSB(BME280_TEMPERATURE_2_MSB_REG, BME280_TEMPERATURE_2_LSB_REG )
   C_PRE[0] = read_LSB_MSB(BME280_PRESSURE_0_MSB_REG, BME280_PRESSURE_0_LSB_REG)
   C_PRE[1] = -10677
   C_PRE[2] = read_LSB_MSB(BME280_PRESSURE_2_MSB_REG, BME280_PRESSURE_2_LSB_REG)
   C_PRE[3] = read_LSB_MSB(BME280_PRESSURE_3_MSB_REG, BME280_PRESSURE_3_LSB_REG)
   C_PRE[4] = -88
   C_PRE[5] = -10
   C_PRE[6] = read_LSB_MSB(BME280_PRESSURE_6_MSB_REG, BME280_PRESSURE_6_LSB_REG)
   C_PRE[7]= -10230
   C_PRE[8] = read_LSB_MSB(BME280_PRESSURE_8_MSB_REG, BME280_PRESSURE_8_LSB_REG)
   C_HUM[0] = read_data(BME280_HUMIDITY_0_CHR_REG)
   C_HUM[1] = read_LSB_MSB(BME280_HUMIDITY_1_MSB_REG, BME280_HUMIDITY_1_LSB_REG)
   C_HUM[2] = read_data(BME280_HUMIDITY_2_CHR_REG)
   C_HUM[3] = ( read_data(BME280_HUMIDITY_3_MSB_REG) << 4 ) | ( read_data(BME280_HUMIDITY_3_LSB_REG) & 0xF )
   C_HUM[4] = ( read_data(BME280_HUMIDITY_4_MSB_REG) << 4 ) | ( read_data(BME280_HUMIDITY_3_LSB_REG) >> 4 )
   C_HUM[5] = read_data(BME280_HUMIDITY_5_CHR_REG)


def BME280_Set_Pressure(value):
   global BME280_MEAS_REG
   getMeasurement = BME280_get( BME280_MEAS_REG )
   getMeasurement &= ~ 0x1C
   getMeasurement |= value << 2
   write_data( BME280_MEAS_REG, getMeasurement )

def BME280_Set_Temperature(value):
    global BME280_MEAS_REG
    getMeasurement = BME280_get( BME280_MEAS_REG )
    getMeasurement &= ~ 0xE0
    getMeasurement |= value << 5
    write_data( BME280_MEAS_REG, getMeasurement )

def BME280_Set_Humidity(value):
    global BME280_HUMIDITY_REG
    write_data( BME280_HUMIDITY_REG, value )

def BME280_Set_Mode(value):
   global BME280_MEAS_REG
   getMeasurement = BME280_get( BME280_MEAS_REG )
   getMeasurement |= value
   write_data( BME280_MEAS_REG, getMeasurement )

def BME280_IsMeasuring():
   status = BME280_get( BME280_STATUS )
   return status &  0x08

def BME280_Compensate_Temperature():
   global TEMPERATURE_DATA
   global C_TMP,FINE
   temp1 = (TEMPERATURE_DATA/8) - (C_TMP[0]*2 )
   temp1=  ( temp1 * C_TMP[1] ) / 2048
   temp2 = (TEMPERATURE_DATA /16) - C_TMP[0]
   temp2 = temp2 * temp2 / 4096
   temp2 = (temp2 * 50) /16384
   FINE = temp1 + temp2
   T = (FINE * 5 + 128) / 256
   return T;

def BME280_Compensate_Humidity():
   global HUMIDITY_DATA
   global FINE,C_HUM
   h1 = FINE - 76800
   h2 = (HUMIDITY_DATA * 16384) - (C_HUM[3] * 1024 *1024) - (C_HUM[4] * h1)
   h2 = (h2 + 16384)/ 32768
   h3 = (((((h1 * C_HUM[5]) / 1024)*(((h1 * C_HUM[2]) / 2048) + 32768)) /1024 + 2097152)* C_HUM[1] + 8192)/ 16384
   h1 = h2 * h3
   h1 = (h1 - (((((h1 / 32768) * (h1 / 32768))/ 128) * C_HUM[0]) / 16))
   if(h1 < 0):
       h1 = 0
   if (h1 > 419430400):
       h1 = 419430400
   h1= h1 / 4096
   return h1

def BME280_Compensate_Pressure():
   global C_PRE,FINE,PRESSURE_DATA
   press1 = (FINE >> 1) - 64000
   press2 = (((press1>>2) * (press1>>2)) >> 11 ) * (C_PRE[5])
   press2 = press2 + ((press1*(C_PRE[4]))<<1)
   press2 = (press2 >> 2)+((C_PRE[3])<<16)
   press1 = (((C_PRE[2] * (((press1>>2) * (press1>>2)) >> 13 )) >> 3) + (((C_PRE[1]) * press1)>>1))>>18
   press1 =((((32768+press1))*(C_PRE[0]))>>15)
   if (press1 == 0):
        return 0
   P = ((((1048576)-PRESSURE_DATA)-(press2>>12)))*3125
   if (P < 0x80000000):
        P = (P << 1) / press1
   else:
        P = (P / press1) * 2

   press1 = ((C_PRE[8]) * ((((P>>3) * (P>>3))>>13)))>>12
   press2 = ((P>>2) * (C_PRE[7])) >> 13
   P = (P + ((press1 + press2 + C_PRE[6]) >> 4))
   return P

def BME280_GetTemperature():
   print "Temperature:  ", BME280_Compensate_Temperature() / 100


def BME280_GetHumidity():
   print "Humidity:  ", BME280_Compensate_Humidity()  / 1020

def BME280_GetPressure():
   print "Pressure:  ", BME280_Compensate_Pressure()  / 100

def BME280_init():
    BME280_Set_Pressure(0x05)
    BME280_Set_Temperature(0x02)
    BME280_Set_Humidity(0x01)
    BME280_Set_Mode(0x03)

# start main
BME280_reset()
BME280_init()
init_weather()
BME280_ReadCalibration()

while True:
  out = BME280_IsMeasuring()
  while out:
     out = BME280_IsMeasuring()

  BME280_read_Measurements()
  BME280_GetTemperature()
  BME280_GetHumidity()
  BME280_GetPressure()
  print "        "
  time.sleep(2)
