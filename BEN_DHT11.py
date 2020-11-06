import Adafruit_DHT
import time 
DHT_SENSOR = Adafruit_DHT.DHT11 
DHT_PIN = 20
t = None 
h = None 
def readDHT():
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN ) 
        return humidity,temperature


