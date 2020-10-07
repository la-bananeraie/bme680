import board
import busio
import adafruit_bme680
import time
import csv
from pytz import timezone
from datetime import datetime
from influxdb import InfluxDBClient

# Sensor configuration
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# influxdb configuration
ifdb   = "air_monitoring" # created database name
ifhost = "192.168.42.40" # raspberry pi 4 ip address, where influx is installed
ifport = 8086 # default port for influxdb
ifclient = InfluxDBClient(ifhost, ifport, None, None, ifdb)

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

        readoutwriter.writerow([now, temperature, humidity, pressure, altitude, gas])

        data = [{
            "measurement": "bme680_data",
            "time": datetime.utcnow(),
            "fields": {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "altitude": altitude,
                "gas": gas,
            }
        }]

        ifclient.write_points(data)

        time.sleep(1)

# 		print('Temperature: {} degrees F'.format(temperature))
# 		print('Humidity: {}%'.format(humidity))
# 		print('Pressure: {}hPa'.format(pressure))
# 		print('Altitude: {} meters'.format(altitude))
# 		print('Gas: {} ohms'.format(gas))
	