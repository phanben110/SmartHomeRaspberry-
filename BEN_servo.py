
import RPi.GPIO as GPIO
import time

servoPIN1 = 26
servoPIN2 = 19 
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)
def servo1() :
    servoPIN1 = 26
    ervoPIN2 = 19 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN1, GPIO.OUT)
    GPIO.setup(servoPIN2, GPIO.OUT)
    p = GPIO.PWM(servoPIN1, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    try:
        p.ChangeDutyCycle(6.7)
        print 7.5 
        #time.sleep(0.5)
        #p.ChangeDutyCycle(10)
        #print 10 
        time.sleep(0.5)
        p.ChangeDutyCycle(13)
        print (12.5) 
        #time.sleep(0.5)
        #p.ChangeDutyCycle(10)
        time.sleep(3)
        p.ChangeDutyCycle(6.7)
        time.sleep(0.5)
    except KeyboardInterrupt:
      p.stop()
      GPIO.cleanup()
      return 1 

def servo2(status) :
    servoPIN1 = 26
    servoPIN2 = 19 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN1, GPIO.OUT)
    GPIO.setup(servoPIN2, GPIO.OUT)
    p = GPIO.PWM(servoPIN2, 50) # GPIO 17 for PWM with 50Hz
    p.start(8) # Initialization
    
    try:
        if status == "on" : 

            p.ChangeDutyCycle(2)
    
        #time.sleep(0.5)
        #p.ChangeDutyCycle(10)
        #print 10 
            time.sleep(0.5)
        #p.ChangeDutyCycle(10)
        else: 

        #time.sleep(0.5)
        #p.ChangeDutyCycle(10)
            p.ChangeDutyCycle(8)
            time.sleep(0.5)
    except KeyboardInterrupt:
      p.stop()
      GPIO.cleanup()
      return 1

