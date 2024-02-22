# Smart Home sensor program
# MicroPython and ESP32 https://docs.micropython.org/en/latest/esp32/quickref.html
# https://docs.micropython.org/en/latest/library/espnow.html
# https://randomnerdtutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/
 
import network
import espnow

from machine import Pin
import time

from hcsr04 import HCSR04              # The HC-SR04 module

########################################
# OWN MODULES
from adc_sub import ADC_substitute

########################################
# CONFIGURATION
dashboard_mac_address = b'\xA1\xB2\xC3\xD4\xE5\xF6' # MAC address of dashboard (Educaboard). Byte string format!

# Sensor
sensor_id = "Ultrasound"               # The sensor ID
pin_us_trigger = 32                    # The ultra sound digital trigger GPIO output pin
pin_us_echo = 33                       # The ultra sound digital echo GPIO input pin

# Battery
pin_battery = 34                       # The battery measurement input pin, ADC1_6

########################################
# OBJECTS
# ESP-NOW
sta = network.WLAN(network.STA_IF)     # Or network.AP_IF
sta.active(True)                       # WLAN interface must be active to send()/recv()

en = espnow.ESPNow()                   # ESP-NOW object
en.active(True)                        # Make ESP-NOW active

# Sensor
sensor = HCSR04(pin_us_trigger, pin_us_echo, 10000) # 10 ms time out

# Battery
batttery = ADC_substitute(pin_battery) # The battery object

########################################
# VARIABLES
# Previous values
prev_sensor_value = -999               # The previous value from the sensor
prev_bat_pct = -1                      # The previous battery percentage value

########################################
# FUNCTIONS
def get_battery_percentage():          # The battery voltage percentage
    adc_at_0_percent = 1450
    adc_at_100_percent = 1766
    min_battery_voltage = 3.0
    max_battery_voltage = 4.2
    adc_value = batttery.read_adc()
    
    voltage_range_per_unit_adc = (max_battery_voltage - min_battery_voltage) / (adc_at_100_percent - adc_at_0_percent)
    
    voltage = (adc_value - adc_at_0_percent) * voltage_range_per_unit_adc + min_battery_voltage
    
    battery_percentage = ((voltage - min_battery_voltage) / (max_battery_voltage - min_battery_voltage)) * 100
    battery_percentage = round(int(battery_percentage))
    if battery_percentage < 0 or battery_percentage > 100:
        battery_percentage = "Error"
        
    return battery_percentage

########################################
# PROGRAM

# INITIALIZATION
# ESP-NOW
en.add_peer(dashboard_mac_address)     # Must add_peer() before send()
en.send(dashboard_mac_address, sensor_id + " ready", False)

print(sensor_id + " ready")

# MAIN (super loop)
while True:
    # Measure the battery percentage
    bat_pct = get_battery_percentage()

    # Check the sensor
    sensor_value = sensor.distance_cm()

    # Send data if there is a change (this principle saves power)
    if bat_pct != prev_bat_pct or sensor_value != prev_sensor_value:
        data_string = str(time.ticks_ms()) + '|' + str(bat_pct) + '|' + str(sensor_value) # The data to send. CHANGE IT!

            
        print("Sending: " + data_string)
        time.sleep(1)
        try:
#             en.send(dashboard_mac_address, data_string, False)
#             print("Sent OK")
            ...
        except ValueError as e:
            print("Error sending the message: " + str(e))  
        
        # Update the previous values for use next time
        prev_bat_pct = bat_pct
        prev_sensor_value = sensor_value
    
    time.sleep_ms(20)                  # Needed to avoid spurious measurements. Min 20 ms