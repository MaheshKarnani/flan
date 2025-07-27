#initialize sensors etc.
import qwiic_rfid
import serial
import time as tim
import sys
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from datetime import datetime, date, timedelta, time
import pandas as pd
import os
import qwiic_tca9548a
import PyNAU7802
import smbus2
import json
import requests
from github import Github, InputGitTreeElement
import keyboard
  #serial to arduino
ser = serial.Serial('/dev/ttyUSB0', 115200)
tim.sleep(2)
print("WASH!")
while True:
    s=float(input("Type FOOD LINE number and press enter."))
    if s==1:
        ser.write(str.encode('e'))
    elif s==2:
        ser.write(str.encode('f'))
    elif s==3:
        ser.write(str.encode('g'))
    elif s==4:
        ser.write(str.encode('h'))
