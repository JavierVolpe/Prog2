import RPi.GPIO as GPIO
from gpiozero import LED
import time
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

red = LED(12)

print('Starting up the PIR Module (click on STOP to exit)')
time.sleep(1)
print ('Ready')

while True:
  if GPIO.input(PIR_PIN):
    print('Motion Detected')
    red.on()
    time.sleep(0.5)
    red.off()
    

  time.sleep(0.5)
