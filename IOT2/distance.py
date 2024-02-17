from hcsr04 import HCSR04
from time import sleep

ultrasonic = HCSR04(15, 34)



while True:
    
    distance_lcd = str(round(ultrasonic.distance_cm(), 2)) + " CM"
    print(f"Distance: {distance_lcd} CM")
    sleep(0.5)



