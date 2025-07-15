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
start_date=date(2025,7,14) 
marker_times=[datetime(2025,7,17,12,0,0), datetime(2025,7,18,12,0,0)]#add important dates here to add vertical lines on last plot
last_date=date.today() #OR TYPE DESIRED DATE ON NEXT LINE AND UNCOMMENT IT
# last_date=date(2025,4,8)
datetag=str(last_date)
known_tags=[1111110209209,1111110252252,1111111151150,1111111134135,196471892,19647186244,19645782,19644148217]
filtermin=15 #lower limit in g
filtermax=35 #upper limit in g 
d=last_date-start_date
days_to_plot=d.days
loadpath="/home/maheshkarnani/Documents/Data/flan_pilot/flan1/"

data_coll_weight = pd.read_csv(loadpath + str(start_date) + "_weights.csv") 
data_coll_events = pd.read_csv(loadpath + str(start_date) + "_events.csv")
data_unit5_coll=data_coll_weight.loc[data_coll_weight['Unit'] == 5] 
b=len(known_tags)
for j in range(days_to_plot):
    day=start_date+timedelta(days = j+1) 
    data = pd.read_csv(loadpath + str(day) + "_weights.csv") 
    frames=[data_coll_weight,data]
    data_coll_weight=pd.concat(frames)
    data_unit5=data.loc[data['Unit'] == 5] 
    if data_unit5.empty:
        print('no manual')
    else:
        frames=[data_unit5_coll,data_unit5.iloc[::-1]]
        data_unit5_coll=pd.concat(frames)
        print(data_unit5_coll)
    data = pd.read_csv(loadpath + str(day) + "_events.csv") 
    frames=[data_coll_events,data]
    data_coll_events=pd.concat(frames)
#data_coll.to_csv (r'/home/flan2/Documents/Data/flan2/export_dataframe.csv', index = None, header=True)
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
    ax1.plot(x , filtered_minmax['Weight'], linestyle='-', marker='o', color=[i/len(known_tags), 1-i/len(known_tags), 1-i/len(known_tags), .3], linewidth=3)
    filtered_an = data_unit5_coll.loc[data_unit5_coll['Animal'] == known_tags[i]] 
    y=filtered_an['Weight']
    x=mdates.datestr2num(filtered_an['Start_Time']) 
    ax1.plot(x, y , linestyle='-', marker='s', color=[i/b, 1-i/b, 1-i/b, .9],linewidth=1,label="manual")
ax1.set_ylabel("weight, g")
ax1.set_xticklabels(x,rotation=30,ha='right')
fmt=mdates.DateFormatter('%m-%d %H:%M:%S')
ax1.xaxis.set_major_formatter(fmt)
plt.grid()
plt.subplots_adjust(bottom=0.15)
plt.show()
