import board
import busio
import adafruit_bme680
import time
import csv
from pytz import timezone
from datetime import datetime

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

tz = timezone('America/Los_Angeles')
with open('readout.csv', 'a+', newline='') as csvfile:
	readoutwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	while True:
		now = datetime.now(tz)
	
		sensor.seaLevelhPa = 30
		temperature = round((sensor.temperature * 1.8000) + 32, 2)
		humidity = round(sensor.humidity, 2)
		pressure = round(sensor.pressure, 2)
		altitude = round(sensor.altitude, 3)
		gas = sensor.gas

# 		print('Temperature: {} degrees F'.format(temperature))
# 		print('Humidity: {}%'.format(humidity))
# 		print('Pressure: {}hPa'.format(pressure))
# 		print('Altitude: {} meters'.format(altitude))
# 		print('Gas: {} ohms'.format(gas))
	
		readoutwriter.writerow([now, temperature, humidity, pressure, altitude, gas])
		time.sleep(3)


