import RPi.GPIO as GPIO 
import time

livingRoom = 17
bedRoom    =5 
kitchen    =  14
toiletRoom =6 
outside    =13 

fan1       = 27 
fan2       = 00
coil       = 12

GPIO.setwarnings ( False ) 

def deviceRoom( room , status ): 
    GPIO.setmode( GPIO.BCM ) 
    GPIO.setup(room, GPIO.OUT )
    if status == 1: 
        GPIO.output(room, True )


    else : 
        GPIO.output(room , False )
def readDevice(pin): 
    GPIO.setmode( GPIO.BCM ) 
    GPIO.setup(pin, GPIO.IN )
    ben = GPIO.input(pin) 
    return ben
    
    
