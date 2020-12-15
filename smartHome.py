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
waterSensor = 27
fan  = 24
coil = 12
sensor = 21 
BLYNK_AUTH = '624362b2c01847f5adedaca933b93c9b'
blynk = BlynkLib.Blynk(BLYNK_AUTH)
value1 = 0 

#this line is comand

@blynk.on("V1")
def v1_write_handler( value1 ): 
    print("light 1 is :{}".format(value1[0]))
    blynk.virtual_write(1, value1[0] )
    blynk.virtual_write(7, value1[0] )
    IO.deviceRoom(livingRoom ,int( value1[0]) )

@blynk.on("V2")
def v2_write_handler( value1 ): 
    print("light 2 is :{}".format(value1[0]))
    blynk.virtual_write(2 ,value1[0] )
    blynk.virtual_write(7, value1[0] )
    IO.deviceRoom(kitchen ,int( value1[0]) )

@blynk.on("V3")
def v3_write_handler( value1 ): 
    print("light 3 is :{}".format(value1[0]))
    blynk.virtual_write(3 ,value1[0] )
    blynk.virtual_write(7, value1[0] )
    IO.deviceRoom(toiletRoom ,int( value1[0]) )
@blynk.on("V4")
def v4_write_handler( value1 ): 
    print("light 4 is :{}".format(value1[0]))
    blynk.virtual_write(4 ,value1[0] )
    blynk.virtual_write(7, value1[0] )
    IO.deviceRoom(outside ,int( value1[0]) )
@blynk.on("V5")
def v5_write_handler( value1 ): 
    print("light 5 is:{}".format(value1[0]))
    blynk.virtual_write(5 ,value1[0] )
    blynk.virtual_write(7, value1[0] )
    IO.deviceRoom(bedRoom ,int( value1[0]) )
@blynk.on("V6")
def v1_write_handler( value1 ): 
    print("fan :{}".format(value1[0]))
    blynk.virtual_write(6 ,value1[0] )
    blynk.virtual_write(7, value1[0] )
    IO.deviceRoom(fan ,int( value1[0]) )
@blynk.on("V7")
def v1_write_handler( value1 ): 
    print("all device are :{}".format(value1[0]))
    blynk.virtual_write(7 ,int (value1[0]) )
    blynk.virtual_write(1, value1[0] )

    controlAllLight( int (value1[0]) ) 

    
@blynk.on("V8")
def v1_write_handler( value1 ): 
    print("window is :{}".format(value1[0]))
    blynk.virtual_write(7, value1[0] )
    if value1[0] == '1' :
        window.servo2(1)
        print 2 

    elif value1[0] == '0' :  
        window.servo2(0)
        print 4 

    blynk.virtual_write(8 ,value1[0] )
    
reader = simple.SimpleMFRC522()
display = lcddriver.lcd() 
display.lcd_display_string( "project smart home",1) 
display.lcd_display_string("Nguyen Minh Duc EVT", 3)
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
    if status == 1 : 

        IO.deviceRoom( livingRoom ,1 ) 
        IO.deviceRoom( kitchen ,1 ) 
        IO.deviceRoom( toiletRoom ,1 ) 
        IO.deviceRoom( outside ,1 ) 
        IO.deviceRoom( bedRoom ,1 ) 
        IO.deviceRoom( fan ,1 )
        window.servo2(1) 
        for i in range(9) : 
            blynk.virtual_write(i ,1 )

    else: 
        IO.deviceRoom( livingRoom ,0 ) 
        IO.deviceRoom( kitchen ,0 ) 
        IO.deviceRoom( toiletRoom ,0 ) 
        IO.deviceRoom( outside ,0 ) 
        IO.deviceRoom( bedRoom ,0 )
        IO.deviceRoom( fan , 0 ) 
        window.servo2(0) 
        for i in range(9) : 
            blynk.virtual_write(i ,0 )

def showDatetime(): 
    my = datetime.datetime.now() 
    ben ="Time  " + str(  my.hour)  + ":"+ str( my.minute)  + ":"+ str( my.second) 
    ben1 ="Time    " + str(  my.hour)  + ":"+ str( my.minute)  
    blynk.virtual_write(11 , ben1 )
    return ben 
def showDatetimeLCD(): 
    my = datetime.datetime.now() 
    ben ="Time  " + str(  my.hour)  + ":"+ str( my.minute)  + ":"+ str( my.second) 
    ben1 ="Time    " + str(  my.hour)  + ":"+ str( my.minute)  
    display.lcd_display_string( ben ,2 )
    return ben 

def readRFID(): 
        print " now place your tag to write "
        lastID , my = reader.write('ben')
        #lastID , my = reader.write_no_block('ben') 
        print lastID
        print " ok "
        GPIO.cleanup() 
        if lastID == ID :
            print "wecome boss"
            coilTrue() 
            blynk.run()
            blynk.virtual_write(12 ,"WECOME TO BOSS" )
            IO.deviceRoom( livingRoom, 1) 
            window.servo1()
            blynk.virtual_write(1 ,1 )
            IO.deviceRoom( kitchen , 1) 
            blynk.virtual_write(2 ,1 )
            display.lcd_display_string("WECOME TO BOSS  ", 4)
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

def setup() : 
    for i in range (8): 
        blynk.virtual_write(i , 0)
        if i == 7 : 
            pass 
    blynk.virtual_write(7,1) 
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
        blynk.virtual_write(10 , temperature )
        if temperature >= 32 : 
            IO.deviceRoom(fan ,int( value1[0]) )


        dht = "hum " + str(humidity) + " temp: " + str(temperature)
        display.lcd_display_string(dht , 1 )
        
        
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
      print('Failed to get reading. Try again!')
    


controlAllLight( False ) 
timebegin = time.time() 
setup()
readDHT()
countWater = 0 
while (True ) :

    
    blynk.run()
        #blynk.notify("hello") 
    ben = IO.readDevice(sensor) 
    water = IO.readDevice( waterSensor )
    if water == 0 and countWater <=2  :
        countWater +=1 

        blynk.notify( "WARING! sky being rain"  ) 

        window.servo2(0)
    if ben == False :
        readRFID()
    if time.time() - timebegin >= 60 :
        readDHT()
        timebegin = time.time()
        showDatetime()
    if time.time() - timebegin >= 150 : 
        countWater = 0 
   

    showDatetimeLCD () 
