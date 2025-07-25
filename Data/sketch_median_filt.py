import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
import pandas as pd
from IPython.display import display
from datetime import datetime, date, timedelta, time
import matplotlib.dates as mdates
import statistics

loadpath="/home/user/Documents/Data/flan1/"
known_tags=[1111110209209,1111110252252,1111111151150,1111111134135,196471892,19647186244,19645782,19644148217]
# known_tags=[19645674,19647181251,1964711262,11111114041,1111110190190,1111110192192,1111111248249,11111116362]
known_tags=[str(tag) for tag in known_tags]

# data_date=date(2025,7,20)

#concatenate
start_date=date(2025,7,18) 
# marker_times=[datetime(2025,7,17,12,0,0), datetime(2025,7,18,12,0,0)]#add important dates here to add vertical lines on last plot
# last_date=date.today() #OR TYPE DESIRED DATE ON NEXT LINE AND UNCOMMENT IT
last_date=date(2025,7,24)
datetag=str(last_date)
d=last_date-start_date
days_to_plot=d.days
data_coll_weight = pd.read_csv(loadpath + str(start_date) + "_weights.csv")

for j in range(days_to_plot):
    day=start_date+timedelta(days = j+1) 
    data = pd.read_csv(loadpath + str(day) + "_weights.csv") 
    frames=[data_coll_weight,data]
    data_coll_weight=pd.concat(frames)

df=data_coll_weight
df['Start_Time']=pd.to_datetime(df['Start_Time'])
df['Animal']=df['Animal'].astype(str)
print(df)

plt.figure(figsize=(20,6))
plt.title(f"FLAN1 Weight Data", fontsize =14)
list_x=[]
list_weights=[]

for rfid in known_tags: #for loop across animals
    print(rfid)
    animal_weights=df[df['Animal']==rfid]['Weight'].values
    animal_times=df[df['Animal']==rfid]['Start_Time'].values
    print(animal_times)
    init_prctile=np.percentile(animal_weights[0:99],80)
    keep_i=[]
    rolling_i=[]
    for i in range(99): #for loop to exclude outliers in first window
        weight=animal_weights[i]
        if weight<1.1*init_prctile and weight>0.9*init_prctile:
            keep_i.append(i)
            rolling_i.append(i)
    rolling_median=np.median(animal_weights[rolling_i])
    print(keep_i)
    rolling_medians=[]
    for i in range(len(keep_i)):
        rolling_medians.append(rolling_median) 
    for j in range(len(animal_weights[100:])): #for loop rolling through data
        weight=animal_weights[j+100]
        if weight<1.2*rolling_median and weight>0.8*rolling_median:
            keep_i.append(j+100)
            rolling_i.pop(0)
            rolling_i.append(j+100)
            rolling_median = np.median(animal_weights[rolling_i])
            rolling_medians.append(rolling_median) 
#             print(rolling_median)
    print(keep_i)
    x = animal_times[keep_i]
    plt.plot(x, rolling_medians, label=str(rfid), marker='o', linestyle = '-', alpha=0.3)
    list_x.append(x)
    list_weights.append(rolling_medians)

print(x)
print(list_x)
plt.ylabel("Weight (g)")
plt.xlabel("Time")
plt.xticks(rotation=30, ha='right')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))
plt.grid(True)
# plt.show()

plt.figure(figsize=(20,6))
plt.title(f"FLAN1 Weight Data", fontsize =14)

list_daily_w=[]
an=-1
for rfid in known_tags: #for loop across animals
    an=an+1
    data={
        "Date":list_x[an],
        "Weight":list_weights[an]
        }
    print(data)
    filtered_df=pd.DataFrame(data)
    print(filtered_df)
    # filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    daily_avg=filtered_df.groupby(pd.Grouper(key='Date', freq='D')).mean().reset_index()
    print(daily_avg)
    x=daily_avg['Date']
    y=daily_avg['Weight']
    print(x)
    print(y)
    plt.plot(x,y, marker='o', linestyle = '-', alpha=0.5)
    list_daily_w.append(daily_avg['Weight'].values)
# print(list_daily_w)
grand_avg=np.mean(list_daily_w, axis=0)
print(grand_avg)
# x=[0,1,2,3,4,5,6,7]
print(x)
plt.plot(x,grand_avg, marker='s', linestyle = '-', alpha=0.8, color='black', linewidth=2)
plt.show()
