from bluepy import btle
from time import sleep

sensor = btle.Peripheral('54:6C:0E:79:23:85')

on_val = '\x01'
off_val = '\x00'

# should enable all features of accelerometer
accel_on_val = '\x7F\x02'
print(accel_on_val)

ir_conf_addr = 0x27
ir_data_addr = 0x24

light_conf_addr = 0x47
light_data_addr = 0x44

humid_conf_addr = 0x2F
humid_data_addr = 0x2C

accel_conf_addr = 0x3F
accel_data_addr = 0x3C

# Turn on IR temperature sensing
sensor.writeCharacteristic(ir_conf_addr, on_val, withResponse=True)
# Turn on Humidity info
sensor.writeCharacteristic(humid_conf_addr, on_val, withResponse=True)
# Turn on Light info
sensor.writeCharacteristic(light_conf_addr, on_val, withResponse=True)
# Turn on Accelerometer info
sleep(2)
sensor.writeCharacteristic(accel_conf_addr, accel_on_val, withResponse=True)

#convert humidity to a human-readable number
def hum_conv(h_data):
	# last two bytes of data contain humidity data
	msb = ord(h_data[3])
	lsb = ord(h_data[2])
	# shift the first byte forward 8 places
	msb_s = msb << 8
	result = msb_s + lsb
	#remove status bits
	result &= ~0x0003
	hum_result = (float(result) / 65536) * 100
	print '%s Percent Relative Humidity' % hum_result

# Convert temp to human-readable
def temp_conv(t_data):
	msb = ord(t_data[3])
	lsb = ord(t_data[2])
	c = ((msb * 256 + lsb) / 4) * 0.03124
	f = c * 9 / 5.0 + 32
	print '%s degrees F' % round(f, 2)

# Read in data from Light sensor and convert the results
# into LUX
def lux_conv(l_data):
	r = ord(l_data[0])
	r2 = ord(l_data[1]) << 8
	r = r + r2	
	m = r & 0x0FFF
	e = (r & 0xF000) >> 12
	if e == 0:
		e = 1
	else:
		e = (2 << (e - 1))
	result = float(m) * (0.01 * float(e))
	print '%s LUX' % round(result, 2)

#Convert data read in from accelerometer
def accel_conv(a_data):
	g_x1 = ord(a_data[0])
	g_x2 = ord(a_data[1])
	g_y1 = ord(a_data[2])
	g_y2 = ord(a_data[3])
	g_z1 = ord(a_data[4])
	g_z2 = ord(a_data[5])
	acc_x1 = ord(a_data[6])
	acc_x2 = ord(a_data[7])
	acc_y1 = ord(a_data[8])
	acc_y2 = ord(a_data[9])
	acc_z1 = ord(a_data[10])
	acc_z2 = ord(a_data[11])
	# add upper and lower half of 16 bits after shifting msb
	acc_x = acc_x1 + (acc_x2 << 8)
	acc_y = acc_y1 + (acc_y2 << 8)
	acc_z = acc_z1 + (acc_z2 << 8)
	gyro_x = g_x1 + (g_x2 << 8)
	gyro_y = g_y1 + (g_y2 << 8)
	gyro_z = g_z1 + (g_z2 << 8)
	print '%s Accel X (G)' % round(((float(acc_x) * 1.0) / (32768 / 16)), 2)
	print '%s Accel Y (G)' % round(((float(acc_y) * 1.0) / (32768 / 16)), 2)
	print '%s Accel Z (G)' % round(((float(acc_z) * 1.0) / (32768 / 16)), 2)

sleep(1)

for i in range(30):
	t_data = sensor.readCharacteristic(ir_data_addr)
	temp_conv(t_data)
	l_data = sensor.readCharacteristic(light_data_addr)
	lux_conv(l_data)
	h_data = sensor.readCharacteristic(humid_data_addr)
	hum_conv(h_data)
	a_data = sensor.readCharacteristic(accel_data_addr)
	accel_conv(a_data)
	sleep(2)

sensor.writeCharacteristic(ir_conf_addr, off_val, withResponse=True)
sensor.writeCharacteristic(light_conf_addr, off_val, withResponse=True)
sensor.writeCharacteristic(humid_conf_addr, off_val, withResponse=True)
sensor.writeCharacteristic(accel_conf_addr, off_val, withResponse=True)

