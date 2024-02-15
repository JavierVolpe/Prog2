# Purpose: Read temperature and humidity from DHT11 sensor and write to database
import Adafruit_DHT
from datetime import datetime
from time import sleep

# Getting the current date and time

import sqlite3


# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

pin = '16'

conn = sqlite3.connect('minDB.db')
cur = conn.cursor()

while True:
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            dt = datetime.now()
            print(dt, end=' ')
            print(' Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

            data = (dt, temperature, humidity)
            query = f"INSERT INTO vejr (datetime, temperature, humidity) VALUES ('{data[0]}', {data[1]}, {data[2]});"

            try:

                cur.execute(query)
                conn.commit()
            except sqlite3.Error as e:
                print(f'Error calling SQL: "{e}"')

                
            finally:
                sleep(1)
                
        else:
            print('Failed to get reading. Try again!')
    except KeyboardInterrupt:
        print('Connection closed')
        conn.close()
        break


