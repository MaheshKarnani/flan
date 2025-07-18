#remove spouts, run this code,
#touch a spout till you get 1ml out
#scan test tag to find out how many drops it was.
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
 #digital lines to arduino for food selection
food_select1 = DigitalOutputDevice(19)
food_select2 = DigitalOutputDevice(26)
food_select1.off()
print('spout1 swap line LOW')
# food_select1.on()
# print('spout1 swap line HIGH')
food_select2.off()
print('spout2 swap line LOW')
# food_select2.on()
# print('spout2 swap line HIGH')

#Initialization routine
mode=1 #experiment mode 0=habituation, 1=variable, 2=induction, 3=post, 4=induction_repeat, 5=post_repeat
swap_threshold=553 #how many drops before covert swap
#load scale calibration files
scale_cal_filepath="/home/flan2/Documents/Data/ScaleCal.json"
scale_tare_filepath="/home/flan2/Documents/Data/ScaleTare.json"
with open(scale_cal_filepath, 'r') as file:
    scale_cal=json.load(file)
with open(scale_tare_filepath, 'r') as file:
    scale_tare=json.load(file)
#initialize qwiic hardware
def enable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.enable_channels(port)
def disable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.disable_channels(port)
def initialize_mux(address):
    mux = qwiic_tca9548a.QwiicTCA9548A(address=address)
    return mux
def create_instance():
    mux = []
    addresses = [*range(0x70, 0x77 + 1)]
    for address in addresses:
        instance = initialize_mux(address)
        if not instance.is_connected():
            continue
        print("Connected to mux {0} \n".format(address))
        instance.disable_all()
        mux.append({
            "instance": instance,
            "scales": [],
        })
    return mux
def create_bus():
    bus = smbus2.SMBus(1)
    return bus
def initialize_scales(mux):
    scales = []
    bus = create_bus()
    ports = [0, 1, 2, 3, 4]
    for port in ports:
        enable_port(mux, port)
        nau = PyNAU7802.NAU7802()
        if not nau.begin(bus):
            # print(f"NOT CONNECTED TO SCALE: {port} \n")
            disable_port(mux, port)
            continue
        print(f"Connected to port: {port} with mux: {mux.address} \n")
        scales.append({
            "port": port,
            "nau": nau
        })
        disable_port(mux, port)
    print(f"scales initialised: {scales} with mux: {mux.address} \n")
    return scales
def get_reading(mux,port):
    global scale_cal
    scales = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    nau = PyNAU7802.NAU7802()
    if not nau.begin(bus):
        # print(f"NOT CONNECTED TO SCALE: {port} \n")
        disable_port(mux, port)
    nau.setCalibrationFactor(scale_cal[port])
    nau.setZeroOffset(scale_tare[port])
    weight=nau.getWeight() * 1000
    print("Mass {0:0.3f} g".format(weight))
    disable_port(mux, port)
    bus.close()
    return weight
def scan_tag1(mux,port):
    antennas = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    my_RFID1 = qwiic_rfid.QwiicRFID(0x13)
    if not my_RFID1.begin():
        # print(f"NOT CONNECTED TO : {port} \n")
        disable_port(mux, port)
    tag1 = my_RFID1.get_tag()
#     scan_time = my_RFID.get_prec_req_time()
    disable_port(mux, port)
    bus.close()
    return tag1
def scan_tag2(mux,port):
    antennas = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    my_RFID2 = qwiic_rfid.QwiicRFID(0x12)
    if not my_RFID2.begin():
        # print(f"NOT CONNECTED TO : {port} \n")
        disable_port(mux, port)
    tag2 = my_RFID2.get_tag()
#     scan_time = my_RFID.get_prec_req_time()
    disable_port(mux, port)
    bus.close()
    return tag2
def scan_tag3(mux,port):
    antennas = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    my_RFID3 = qwiic_rfid.QwiicRFID(0x11)
    if not my_RFID3.begin():
        # print(f"NOT CONNECTED TO : {port} \n")
        disable_port(mux, port)
    tag3 = my_RFID3.get_tag()
#     scan_time = my_RFID.get_prec_req_time()
    disable_port(mux, port)
    bus.close()
    return tag3
def scan_tag4(mux,port):
    antennas = []
    bus = create_bus()
    port = port
    enable_port(mux, port)
    my_RFID4 = qwiic_rfid.QwiicRFID(0x1A)
    if not my_RFID4.begin():
        # print(f"NOT CONNECTED TO : {port} \n")
        disable_port(mux, port)
    tag4 = my_RFID4.get_tag()
#     scan_time = my_RFID.get_prec_req_time()
    disable_port(mux, port)
    bus.close()
    return tag4

mux = create_instance()

for i, val in enumerate(mux):
    print(i)
    mux[i]["scales"] = initialize_scales(mux[i]["instance"])
    get_reading(mux[i]["instance"],3)
get_reading(mux[0]["instance"],3)

tag1=int(scan_tag1(mux[0]["instance"],0))
tag2=int(scan_tag2(mux[0]["instance"],1))
tag3=int(scan_tag3(mux[0]["instance"],2))
tag4=int(scan_tag4(mux[0]["instance"],4))
print(tag1)
print(tag2)
print(tag3)
print(tag4)

#RFID detection interrupts
RFID1_detect = DigitalInputDevice(21)
RFID2_detect = DigitalInputDevice(20, pull_up=False)
RFID3_detect = DigitalInputDevice(16) 
RFID4_detect = DigitalInputDevice(12)

  #serial to arduino
ser = serial.Serial('/dev/ttyUSB0', 115200)
tim.sleep(2)



# set initial values, time stamps animal histories.
licks1=0
licks2=0
drinks1=0
drinks2=0
licks3=0
licks4=0
drinks3=0
drinks4=0
tag1=0 #initialize animal
tag2=0
tag3=0
tag4=0
known_tags=[19647231169,
19645674,19647181251,1964711262,11111114041,1111110190190,1111110192192,1111111248249,11111116362]
food_flags=[0,0,0,0,0,0,0,0,0]
food_flags2=[0,0,0,0,0,0,0,0,0]
cumulative1=[0,0,0,0,0,0,0,0,0]
cumulative2=[0,0,0,0,0,0,0,0,0]
cumulative3=[0,0,0,0,0,0,0,0,0]
cumulative4=[0,0,0,0,0,0,0,0,0]

#saving and uploading
savepath="/home/flan2/Documents/Data/"
event_list1 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag1],
    "Unit":1,
    "Licks1" : [licks1],
    "Licks2" : [licks2],
    "Drinks1" : [drinks1],
    "Drinks2" : [drinks2],
}

event_list2 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag2],
    "Unit":2,
    "Licks1" : [licks1],
    "Licks2" : [licks2],
    "Drinks1" : [drinks1],
    "Drinks2" : [drinks2],
}

weight_list = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag3],
    "Unit":3,
    "Weight": [round(float(get_reading(mux[0]["instance"],3)),2)],
}
weight_list2 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag4],
    "Unit":5,
    "Weight": [0],
}
swap_list1 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag1],
    "Unit":1,
    "Drinks1" : [drinks1],
    "Drinks2" : [drinks2],
    "Drinks3" : [drinks3],
    "Drinks4" : [drinks4],
    "Swap_direction" : ["initialize"]
    }
swap_list2 = {
    "Mode" : ["initialize"], 
    "Start_Time": [datetime.now()],
    "Animal": [tag2],
    "Unit":2,
    "Drinks1" : [drinks1],
    "Drinks2" : [drinks2],
    "Drinks3" : [drinks3],
    "Drinks4" : [drinks4],
    "Swap_direction" : ["initialize"]
    }
class SaveData:
    def append_event(self,event_list):
        df_e = pd.DataFrame(event_list)
        datetag=str(date.today())
        if not os.path.isfile(savepath + datetag + "_events.csv"):
            df_e.to_csv(savepath + datetag + "_events.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(savepath + datetag + "_events.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
    def append_weight(self,weight_list):
        df_e = pd.DataFrame(weight_list)
        datetag=str(date.today())
        if not os.path.isfile(savepath + datetag + "_weights.csv"):
            df_e.to_csv(savepath + datetag + "_weights.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(savepath + datetag + "_weights.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
    def append_swap(self,swap_list):
        df_e = pd.DataFrame(swap_list)
        datetag=str(date.today())
        if not os.path.isfile(savepath + datetag + "_swaps.csv"):
            df_e.to_csv(savepath + datetag + "_swaps.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(savepath + datetag + "_swaps.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)

save = SaveData()
save.append_event(event_list1)
save.append_event(event_list2)
save.append_weight(weight_list)
save.append_swap(swap_list1)
save.append_swap(swap_list2)
# save.append_event(event_list4)
event_list1.update({'Mode': [mode]})
event_list2.update({'Mode': [mode]})
weight_list.update({'Mode': [mode]})
weight_list2.update({'Mode': [mode]})
swap_list1.update({'Mode': [mode]})
swap_list2.update({'Mode': [mode]})
# event_list4.update({'Mode': [mode]})
upload_time=datetime.now()
upload_interval=timedelta(hours=6) #minimum interval between uploads, hours suggested
action_time=datetime.now()
action_interval=timedelta(minutes=15) #safe interval from last detection to start upload, 15 min suggested
ser.write(str.encode('d'))
ser.write(str.encode('c'))
# 
# execution loop
#
#experiment routine
while True:
    if RFID4_detect.value == 0:
        print("CALIBRATE")
        s=float(input("Type spout number and press enter."))
        if s==1:
            ser.write(str.encode('a'))
        elif s==2:
            ser.write(str.encode('b'))
        Ard_data = ser.readline()
        Ard_data = Ard_data.decode("utf-8","ignore")
        print(Ard_data)
        licks1,drinks1,licks2,drinks2,e = Ard_data.split(",")  
        event_list1.update({'Licks1':[licks1]})#for previous animal
        event_list1.update({'Licks2':[licks2]})#for previous animal
        event_list1.update({'Drinks1':[drinks1]})#for previous animal
        event_list1.update({'Drinks2':[drinks2]})#for previous animal
        save.append_event(event_list1)#for previous animal
        licks1=0
        licks2=0
        drinks1=0
        drinks2=0
        event_list1.update({'Start_Time': [datetime.now()]})
        event_list1.update({'Animal': [tag1]})
        swap_list1.update({'Start_Time': [datetime.now()]})
        swap_list1.update({'Animal': [tag1]})
        