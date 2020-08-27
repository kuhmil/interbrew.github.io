import os
import glob
import time
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
#from time import sleep
import datetime 
import time
import sqlite3
#import Adafruit_DHT
dbname='interbrew.db'
sampleFreq = 2 # time in seconds
# get data from DHT sensor

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#Sensors
relay_cold = 15
relay_hot = 16
#temp_probe = 13

def blink(pin):
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    #while True: # Run forever
    GPIO.output(pin, GPIO.HIGH) # Turn on
    sleep(1)                  # Sleep for 1 second
    GPIO.output(pin, GPIO.LOW)  # Turn off
    sleep(1)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

#Relays
def relays(relay_change, state):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relay_change, GPIO.OUT)
    GPIO.output(relay_change, state)

now = datetime.datetime.now().replace(second=0, microsecond=0)

def logData (temp):    
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print("reading log")
    curs.execute("INSERT INTO TEMP_data values(datetime('now'), (?))", (temp,))
    #sql = "INSERT INTO sensor_data(datetimes, temp) VALUES (%s, %s)"
    #val = (datetime('now'), temp) 
    #mycursor.execute(sql, val) 
    conn.commit()
    conn.close()
# display database data
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    #print ("\nEntire database contents:\n")
    #for row in curs.execute("SELECT * FROM TEMP_data"):
     #   print (row)
    conn.close()
# main function
def main():
    for i in range (0,3):
        read_temp()
        time.sleep(sampleFreq)
    displayData()

try:
    while True:
        temp_c = read_temp()
        logData(int(temp_c))
       # time.sleep(sampleFreq)
       # print("temperature")
        main()
        print(f"{temp_c} writing temp data to database")
except KeyboardInterrupt:
    GPIO.cleanup()
