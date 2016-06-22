#!/user/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(36,GPIO.IN,pull_up_down=GPIO.PUD_UP)
while True:
    in_value = GPIO.input(36)
    time.sleep(1)
    print in_value

    if in_value == False:
        GPIO.output(35,True)
        time.sleep(1)
    else:
        GPIO.output(35,False)
        time.sleep(1)
