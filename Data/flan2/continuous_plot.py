import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
import pandas as pd
from IPython.display import display
from datetime import datetime, date, timedelta, time
import matplotlib.dates as mdates
import statistics
plt.close('all')

#concatenate
start_date=date(2025,7,15) 
marker_times=[datetime(2025,7,15,12,0,0), datetime(2025,7,18,12,0,0)]#add important dates here to add vertical lines on last plot
last_date=date.today() #OR TYPE DESIRED DATE ON NEXT LINE AND UNCOMMENT IT
# last_date=date(2025,4,8)
datetag=str(last_date)
known_tags=[19645674,19647181251,1964711262,11111114041,1111110190190,1111110192192,1111111248249,11111116362]
filtermin=10 #lower limit in g
filtermax=35 #upper limit in g 
d=last_date-start_date
days_to_plot=d.days
loadpath="/home/maheshkarnani/Documents/Data/flan_pilot/"

data_coll_weight = pd.read_csv(loadpath + str(start_date) + "_weights.csv") 
data_coll_events = pd.read_csv(loadpath + str(start_date) + "_events.csv")
for j in range(days_to_plot):
    day=start_date+timedelta(days = j+1) 
    data = pd.read_csv(loadpath + str(day) + "_weights.csv") 
    frames=[data_coll_weight,data]
    data_coll_weight=pd.concat(frames)
    data = pd.read_csv(loadpath + str(day) + "_events.csv") 
    frames=[data_coll_events,data]
    data_coll_events=pd.concat(frames)
    
#data_coll.to_csv (r'/home/flan2/Documents/Data/export_dataframe.csv', index = None, header=True)
tags=data_coll_weight['Animal']
unique_tags=list(set(tags))
print('found unique tags:')
print(len(unique_tags))

#plot raw
fig1 = plt.figure(figsize=(16, 8))
# plot filtered weights
ax1 = fig1.add_subplot(221)
ax1.set_title(f"all {len(known_tags)} known tags ")
for i in range(len(known_tags)):
    filtered_an = data_coll_weight.loc[data_coll_weight['Animal'] == known_tags[i]] 
    filtered_min = filtered_an.loc[filtered_an['Weight'] > filtermin]
    filtered_minmax =  filtered_min.loc[filtered_min['Weight'] < filtermax]
    display(filtered_minmax.head(20))
    x=mdates.datestr2num(filtered_minmax['Start_Time']) 
    ax1.plot(x , filtered_minmax['Weight'], linestyle='-', marker='o', color=[i/len(known_tags), 1-i/len(known_tags), 1-i/len(known_tags), .3], linewidth=1)
ax1.set_ylabel("weight, g")
ax1.set_xticklabels(x,rotation=30,ha='right')
fmt=mdates.DateFormatter('%m-%d %H:%M:%S')
ax1.xaxis.set_major_formatter(fmt)
plt.grid()
plt.subplots_adjust(bottom=0.15)
plt.show()
