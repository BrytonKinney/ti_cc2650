from bluepy import btle
from time import sleep

sensor = btle.Peripheral('24:71:89:D0:1C:04')

on_val = '\x01'
off_val = '\x00'

# 0x338
# 	00000110       	0111000
#                 ^           	   ^
#    accel range   accel x,y,z enable
accel_on_val = hex(170)

ir_start_addr = 0x27
ir_data_addr = 0x24

light_start_addr = 
light_data_addr = 

humid_start_addr =
humid_data_addr = 

accel_start_addr =
accel_data_addr =

# Turn on IR temperature sensing
sensor.writeCharacteristic(ir_start_addr, on_val, withResponse=True)
# Turn on Humidity info
sensor.writeCharacteristic(humid_start_addr, on_val, withResponse=True)
# Turn on Light info
sensor.writeCharacteristic(light_start_addr, on_val, withResponse=True)
# Turn on Accelerometer info
sensor.writeCharacteristic(accel_start_addr, accel_on_val, withResponse=True)

#convert humidity to human-readable
def h_conv(h_data):
	# last two bytes of data contain humidity data
	msb = ord(h_data[3])
	lsb = ord(h_data[2])
	# shift the first byte forward 8 places, as this is big-endian (I think? haven't found out yet)
	msb_s = msb << 8
	result = msb_s + lsb
	#remove status bits
	result &= ~0x0003
	hum_result = (ord(result) / 65536) * 100
	print '%s % Relative Humidity' % hum_result

# Convert temp to human-readable
def t_conv(t_data):
	msb = ord(t_data[3])
	lsb = ord(t_data[2])
	c = ((msb * 256 + lsb) / 4) * 0.03124
	f = c * 9 / 5.0 + 32
	print '%s degrees F' % round(f, 2)


def l_conv(l_data):
	msb = l_data[1]
	msb_s = msb << 8
	lsb = l_data[0]
	r = msb_s + lsb
	m = r & 0x0FFF
	e = (r & 0xF000) >> 12
	e = 1 if e == 0 else e = (2 << (e - 1))
	result = ord(m) * (0.01 * ord(e))
	print '%s LUX' % round(result, 2)

def a_conv(a_data):
	acc_x1 = a_data[6]
	acc_x2 = a_data[7]
	acc_y1 = a_data[8]
	acc_y2 = a_data[9]
	acc_z1 = a_data[10]
	acc_z2 = a_data[11]
	acc_x = acc_x1 + (acc_x2 << 8)
	acc_y = acc_y1 + (acc_y2 << 8)
	acc_z = acc_z1 + (acc_z2 << 8)
	print '%s Accel X' % round((ord(acc_x) * 1.0) / (32768 / 16)), 2)
	print '%s Accel Y' % round((ord(acc_y) * 1.0) / (32768 / 16)), 2)
	print '%s Accel Z' % round((ord(acc_z) * 1.0) / (32768 / 16)), 2)

sleep(1)

for i in range(30):
	t_data = sensor.readCharacteristic(ir_data_addr)
	t_conv(t_data)
	l_data = sensor.readCharacteristic(light_data_addr)
	l_conv(l_data)
	h_data = sensor.readCharacteristic(humid_data_addr)
	h_conv(h_data)
	a_data = sensor.readCharacteristic(accel_data_addr)
	a_conv(a_data)
	sleep(2)

sensor.writeCharacteristic(ir_start_addr, off_val, withResponse=True)
sensor.writeCharacteristic(light_start_addr, off_val, withResponse=True)
sensor.writeCharacteristic(humid_start_addr, off_val, withResponse=True)
sensor.writeCharacteristic(accel_start_addr, off_val, withResponse=True)

