# Import necessary libraries
import Adafruit_DHT
from datetime import datetime
from time import sleep
import paho.mqtt.publish as publish

# Define sensor type and pin
sensor = Adafruit_DHT.DHT11
pin = '16'
mqtt_host = '52.178.210.165'

# Main loop
while True:
    try:
        # Read temperature and humidity from DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # If readings are valid
        if humidity is not None and temperature is not None:
            # Get current datetime and format it
            dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Prepare payload in the format: datetime|temperature|humidity
            payload = f"{dt}|{temperature}|{humidity}"

            # Print payload for debugging
            print(payload)

            # Publish payload to MQTT topic "stue/data" on the specified host
            publish.single("stue/data", payload, hostname=mqtt_host)

            # Sleep for 1 second before the next reading
            sleep(1)
        else:
            # Print error message if readings are not valid
            print('Failed to get reading. Try again!')
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print('Connection closed')
        break