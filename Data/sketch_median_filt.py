import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
import pandas as pd
from IPython.display import display
from datetime import datetime, date, timedelta, time
import matplotlib.dates as mdates
import statistics

loadpath="/home/user/Documents/Data/"
data_date=date(2025,7,20) 

df=pd.read_csv(loadpath + str(data_date) + "_weights.csv")
df['Start_Time']=pd.to_datetime(df['Start_Time'])
df['Animal']=df['Animal'].astype(str)

known_tags=[1111110209209,1111110252252,1111111151150,1111111134135,
            196471892,19647186244,19645782,19644148217]
known_tags=[str(tag) for tag in known_tags]

for rfid in known_tags: #for loop across animals
    animal_weights=df[df['Animal']==rfid]['Weight'].values
    init_prctile=np.percentile(animal_weights[0:99],80)
    keep_i=[]
    for i in range(99): #for loop to exclude outliers in first window
        weight=animal_weights[i]
        if weight<1.1*init_prctile and weight>0.9*init_prctile:
            keep_i.append(i)    
    rolling_median=np.median(animal_weights[keep_i])
    rolling_i=keep_i
    #print(rolling_median)
    
    for j in range(len(animal_weights[100:])): #for loop rolling through data
        weight=animal_weights[j]
        if weight<1.1*rolling_median and weight>0.9*rolling_median:
            keep_i.append(j)
            rolling_i.pop(0)
            rolling_i.append(j)
            rolling_median = np.median(animal_weights[rolling_i])
            #print(rolling_median)
x = median dates 

plt.figure(figsize=(20,6))
plt.title(f"FLAN1 Weight Data", fontsize =14)
plt.plot(x, rolling_median, label=str(rfid), marker='o', linestyle = '-', alpha=0.8)
pt.ylabel("Weight (g)")
plt.xlabel("Time")
plt.xticks(rotation=30, ha='right')
ax.xaxis.set_major_formatter(mdates.DataFormatter('%m-%d %H:%M:%S'))
plt.grid(True)
plt.show()


plt.show()
