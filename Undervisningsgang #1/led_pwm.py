import RPi.GPIO as GPIO
from gpiozero import PWMLED
import time
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

led = PWMLED(12)


print('Starting up the PIR Module (click on STOP to exit)')
time.sleep(1)
print ('Ready')

while True:
  if GPIO.input(PIR_PIN):
     print('Motion Detected')
     led.value = 1
     time.sleep(1)
     led.value = 0

  time.sleep(1)

