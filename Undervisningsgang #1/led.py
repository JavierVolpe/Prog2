#    2.3 (Se dokumentationen)Prøv at bruge gpiozero til at:
#    - Teste en LED og få den til at blinke og bagefter styre 
#    brightness med PWM


from gpiozero import LED
from time import sleep

red = LED(12)

while True:
    red.on()
    sleep(1)
    red.off()
    sleep(1)