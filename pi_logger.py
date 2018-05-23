import RPI.GPIO as GPIO
import sqlite3
from sqlalchemy import *
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1015()

db = create_engine('sqlite:///valve.db')
db.echo = False
metadata = MetaData(self.db)
valves = Table('valves', metadata,
    Column('valve_1_activated', Integer),
    Column('valve_1_deactivated', Integer),
    Column('valve_2_activated', Integer),
    Column('valve_2_deactivated', Integer),
    Column('valve_3_activated', Integer),
    Column('valve_3_deactivated', Integer),
    Column('valve_4_activated', Integer),
    Column('valve_4_deactivated', Integer)
)

valves.create()

arduino = serial.Serial(
    "COM20",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)

flipped = True
i = 0

valve1array = []
valve2array = []
valve3array = []
valve4array = []

while (True):
    val = GPIO.input(25)
    if (val == 0 and flipped == True):
        if (i == 0):
            valve1array[0] = readAdc(0)
            i++
            flipped = False
        elif (i == 2):
            valve2array[0] = readAdc(1)
            i++
            flipped = False
        elif (i == 4):
            valve3array[0] = readAdc(2)
            i++
            flipped = False
        elif (i == 6):
            valve4array[0] = readAdc(3)
            i++
            flipped = False
    elif (val == 1 and flipped = False):
        if (i == 1):
            valve1array[1] = readAdc(0)
            i++
            flipped = True
        elif (i == 3):
            valve2array[1] = readAdc(1)
            i++
            flipped = True
        elif (i == 5):
            valve3array[1] = readAdc(2)
            i++
            flipped = True
        elif (i == 7):
            valve4array[1] = readAdc(3)
            i = 0
            flipped = True
            saveData()


def readAdc(channel):
    average = 0
    numSamples = 20
    j = 0
    GAIN = 1
    adc.start_adc(channel, gain=GAIN)
    while(j < 1):
        average += adc.get_last_result()
        j++
    average /= numSamples
    adc.stop_adc()
    return average

def saveData():
    obj = createContainer()
    v = valves.insert()
    v.execute(obj)


def createContainer():
    objContainer = {}
    objContainer["valve_1_activated"] = valve1array[0]
    objContainer["valve_1_deactivated"] = valve1array[1]
    objContainer["valve_2_activated"] = valve2array[0]
    objContainer["valve_2_deactivated"] = valve2array[1]
    objContainer["valve_3_activated"] = valve3array[0]
    objContainer["valve_3_deactivated"] = valve3array[1]
    objContainer["valve_4_activated"] = valve4array[0]
    objContainer["valve_4_deactivated"] = valve4array[1]
    return objContainer
