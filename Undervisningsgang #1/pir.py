import RPi.GPIO as GPIO

#TODO import motionsensor?

from time import sleep
 
GPIO.setmode(GPIO.BCM) #Broadcom SOC channel (Raspberry Pi)
GPIO.setwarnings(False)
PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

print('Starting up the PIR Module (click on STOP to exit)')
sleep(1)
print ('Ready')

while True:
  if GPIO.input(PIR_PIN):
    print('Motion Detected')
  sleep(1)