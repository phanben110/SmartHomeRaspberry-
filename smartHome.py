import RPi.GPIO as GPIO 
import SimpleMFRC522 as simple 
import Adafruit_DHT
import lcddriver
import time
import datetime 
from multiprocessing import Process
import BlynkLib 
import BEN_light as IO
import BEN_servo as window 
livingRoom = 17 
bedRoom    = 5
kitchen    = 14 
toiletRoom = 6 
outside    = 13 
fan  = 27
coil = 12
sensor = 21 
BLYNK_AUTH = '624362b2c01847f5adedaca933b93c9b'
blynk = BlynkLib.Blynk(BLYNK_AUTH)
value1 = 0 
@blynk.on("V1")
def v1_write_handler( value1 ): 
    print("light 1 is :{}".format(value1[0]))
    IO.deviceRoom(livingRoom ,int( value1[0]) )

@blynk.on("V2")
def v2_write_handler( value1 ): 
    print("light 2 is :{}".format(value1[0]))
    IO.deviceRoom(kitchen ,int( value1[0]) )

@blynk.on("V3")
def v3_write_handler( value1 ): 
    print("light 3 is :{}".format(value1[0]))
    IO.deviceRoom(toiletRoom ,int( value1[0]) )
@blynk.on("V4")
def v4_write_handler( value1 ): 
    print("light 4 is :{}".format(value1[0]))
    IO.deviceRoom(outside ,int( value1[0]) )
@blynk.on("V5")
def v5_write_handler( value1 ): 
    print("light 5 is:{}".format(value1[0]))
    IO.deviceRoom(bedRoom ,int( value1[0]) )
@blynk.on("V6")
def v1_write_handler( value1 ): 
    print("fan :{}".format(value1[0]))
    IO.deviceRoom(fan ,int( value1[0]) )
@blynk.on("V7")
def v1_write_handler( value1 ): 
    print("all device are :{}".format(value1[0]))
    controlAllLight( value1[0] ) 
@blynk.on("V8")
def v1_write_handler( value1 ): 
    print("window is :{}".format(value1[0]))
    window.servo2(value1[0])
    
reader = simple.SimpleMFRC522()
display = lcddriver.lcd() 
display.lcd_display_string( "project smart home",1) 
display.lcd_display_string("Phan Ben 18TDH1", 3)
x = 0
ID = 166324061428

lastID = None

def coilTrue(): 
    IO.deviceRoom( coil , 1 ) 
    time.sleep (0.2) 
    IO.deviceRoom( coil , 0 ) 
def coilFalse(): 
    for i in range(4):
        IO.deviceRoom( coil , 1) 
        time.sleep(0.05) 
        IO.deviceRoom( coil , 0 )
        time.sleep(0.05)
def controlAllLight(status):
    if status == True : 

        IO.deviceRoom( livingRoom ,1 ) 
        IO.deviceRoom( kitchen ,1 ) 
        IO.deviceRoom( toiletRoom ,1 ) 
        IO.deviceRoom( outside ,1 ) 
        IO.deviceRoom( bedRoom ,1 ) 
        IO.deviceRoom( fan ,1 ) 
    else: 
        IO.deviceRoom( livingRoom ,0 ) 
        IO.deviceRoom( kitchen ,0 ) 
        IO.deviceRoom( toiletRoom ,0 ) 
        IO.deviceRoom( outside ,0 ) 
        IO.deviceRoom( bedRoom ,0 )
        IO.deviceRoom( fan , 0 ) 

def showDatetime(): 
    my = datetime.datetime.now() 
    ben ="Time  " + str(  my.hour)  + ":"+ str( my.minute)  + ":"+ str( my.second) 
    display.lcd_display_string( ben ,2 ) 
    
    blynk.virtual_write(11 , ben )
    return ben 

def readRFID(): 
        print " now place your tag to write " 
        lastID , my = reader.write_no_block('ben') 
        print lastID
        print " ok "
        GPIO.cleanup() 
        if lastID == ID :
            print "wecome boss"
            coilTrue() 
            blynk.run()
            blynk.virtual_write(12 ,"WECOME TO BOSS" )
            IO.deviceRoom( livingRoom, 1) 
            IO.deviceRoom( kitchen , 1) 
            display.lcd_display_string("WECOME TO BOSS  ", 4)
            window.servo1()
        elif lastID is not  ID : 
            
            print  "wrong please try again" 
            coilFalse() 
            TIME  = showDatetime() 
            note = "RFID Wrong " + TIME 

            blynk.virtual_write(12 , "RFID wrong" )
            blynk.notify( note ) 
            for i in range (2) : 
                
                display.lcd_display_string("..............", 4 ) 
                time.sleep(0.1)
                display.lcd_display_string("WRONG, TRY AGAIN", 4)
                time.sleep(0.1)

            time.sleep(1)

def readDHT(): 

    sensor=Adafruit_DHT.DHT11
    gpio= 20 
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temperature is not None:
        blynk.virtual_write(9 , humidity )
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
      print('Failed to get reading. Try again!')
    


controlAllLight( False ) 
timebegin = time.time() 
while (True ) :

    
    blynk.run()
        #blynk.notify("hello") 
    ben = IO.readDevice(sensor) 
    if ben == False :
        readRFID()
    if time.time() - timebegin >= 5 : 
        readDHT()
        timebegin = time.time() 
    showDatetime () 
