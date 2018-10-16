from bluepy import btle
from time import sleep

sensor = btle.Peripheral('24:71:89:D0:1C:04')

on_val = '\x01'
off_val = '\x00'

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
sensor.writeCharacteristic(accel_start_addr, on_val, withResponse=True)

#convert humidity to human-readable
def h_conv(h_data):
	# last two bytes of data contain humidity data
	msb = ord(h_data[3])
	lsb = ord(h_data[2])
	# shift the first byte forward 8 places, as this is big-endian (I think? haven't found out yet)
	lsb_s = lsb << 8
	result = msb + lsb_s
	#remove status bits
	result &= ~0x0003
	hum_result = (result / 65536) * 100
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
	lsb = l_data[0]
	result = msb * (0.01 * lsb)
	print '%s LUX' % round(result, 2)

def a_conv(a_data):
	

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

sensor.writeCharacteristic(ir_start_addr, off_val, withResponse=True)
sensor.writeCharacteristic(light_start_addr, off_val, withResponse=True)
sensor.writeCharacteristic(humid_start_addr, off_val, withResponse=True)
sensor.writeCharacteristic(accel_start_addr, off_val, withResponse=True)

