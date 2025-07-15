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
marker_times=[datetime(2025,7,15,12,0,0), datetime(2025,7,18,12,0,0)]#add important dates here to add vertical lines on last plot
last_date=date.today() #OR TYPE DESIRED DATE ON NEXT LINE AND UNCOMMENT IT
# last_date=date(2025,4,8)
datetag=str(last_date)
known_tags=[19645674,19647181251,1964711262,11111114041,1111110190190,1111110192192,1111111248249,11111116362]
filtermin=10 #lower limit in g
filtermax=35 #upper limit in g 
d=last_date-start_date
days_to_plot=d.days
loadpath="/home/flan2/Documents/Data/"

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
    y=sig.savgol_filter(filtered_minmax['Weight'],
                           50, # window size used for filtering
                           3), # order of fitted polynomial
    ax1.plot(x , y, linestyle='-', marker='', color=[i/len(known_tags), 1-i/len(known_tags), 1-i/len(known_tags), .8], linewidth=5)
    hits.append(len(x))
# ax1.set_ylabel("weight, g")
ax1.set_xticklabels(x,rotation=30,ha='right')
fmt=mdates.DateFormatter('%m-%d %H:%M:%S')
ax1.xaxis.set_major_formatter(fmt)
# 
# # plot filtered weights of known animals and gather averages
# averages=[]
# ax2 = fig1.add_subplot(223)
# ax2.set_title(f"all {len(known_tags)} known tags ")
# for i in range(len(known_tags)):
#     filtered_an = data.loc[data['Animal'] == known_tags[i]] 
#     filtered_min = filtered_an.loc[filtered_an['Weight'] > filtermin]
#     filtered_minmax =  filtered_min.loc[filtered_min['Weight'] < filtermax]
#     # display(filtered_minmax.head(20))
#     x=mdates.datestr2num(filtered_minmax['Start_Time']) 
#     ax2.plot(x , filtered_minmax['Weight'], linestyle='-', marker='o', color=[1/len(known_tags)*i, 1-1/len(known_tags)*i, 1-1/len(known_tags)*i, .5])
#     # ax1.set_xticks(x)
#     if filtered_minmax.empty:
#         # print('empty bin')
#         averages.append(np.nan) 
#     else:
#         averages.append(statistics.mean(filtered_minmax['Weight']))
# # ax2.set_ylabel("weight, g")
# ax2.set_xticklabels(x,rotation=30,ha='right')
# fmt=mdates.DateFormatter('%m-%d %H:%M:%S')
# ax2.xaxis.set_major_formatter(fmt)
# 
# # gather and plot daily averages of known animals
# bw_matrix=[]
# data_unit5_coll=pd.DataFrame(
#     {
#         "Mode": [],
#         "Start_Time": [],
#         "Animal": [],
#         "Weight": [],
#         "Unit": [],
#     }
# )
# pel_matrix=[]
# x=[]
# for j in range(days_to_plot):
#     day=last_date-timedelta(days = j) 
#     data = pd.read_csv(loadpath + str(day) + "_weights.csv") #filter time to 12h bin
#     # plot filtered weights of known animals and gather averages
#     bin1_offset=time(18,0)
#     bin1_centre=datetime.combine(day,bin1_offset)
#     bin1_start_offset=time(12,0)
#     bin1_start=datetime.combine(day,bin1_start_offset)
#     x.append(bin1_centre)
#     bin2_offset=time(6,0)
#     bin2_centre=datetime.combine(day,bin2_offset)
#     x.append(bin2_centre)
#     bw_averages1=[]
#     bw_averages2=[]
#     pel_sums1=[]
#     pel_sums2=[]
#     for i in range(len(known_tags)):
#         filtered_an = data.loc[data['Animal'] == known_tags[i]] 
#         filtered_min = filtered_an.loc[filtered_an['Weight'] > filtermin]
#         filtered_minmax =  filtered_min.loc[filtered_min['Weight'] < filtermax]
#         filtered_time = filtered_minmax.loc[pd.to_datetime(filtered_minmax['Start_Time'], format='%Y-%m-%d %H:%M:%S.%f') > bin1_start]
#         if filtered_time.empty:
#             # print('empty bin')
#             bw_averages1.append(np.nan)
#         else:
#             bw_averages1.append(statistics.median(filtered_time['Weight']))
#         filtered_time = filtered_minmax.loc[pd.to_datetime(filtered_minmax['Start_Time'], format='%Y-%m-%d %H:%M:%S.%f') < bin1_start]
#         if filtered_time.empty:
#             # print('empty bin')
#             bw_averages2.append(np.nan)
#         else:
#             bw_averages2.append(statistics.median(filtered_time['Weight']))
#     bw_matrix.append(bw_averages1)
#     bw_matrix.append(bw_averages2)
#     #next manual measurements
#     data_unit5=data.loc[data['Unit'] == 5] 
#     if data_unit5.empty:
#         print('no manual')
#     else:
#         frames=[data_unit5_coll,data_unit5.iloc[::-1]]
#         data_unit5_coll=pd.concat(frames)
#         # print(data_unit5_coll)
#     #drinking next
#     data = pd.read_csv(loadpath + str(day) + "_events.csv") 
#     for i in range(len(known_tags)):
#         filtered_an = data.loc[data['Animal'] == known_tags[i]] 
#         filtered_time = filtered_an.loc[pd.to_datetime(filtered_an['Start_Time'], format='%Y-%m-%d %H:%M:%S.%f') > bin1_start]
#         if filtered_time.empty:
#             # print('empty bin')
#             pel_sums1.append(np.nan)
#         else:
#             pel_sums1.append(sum(filtered_time['Drinks1']+filtered_time['Drinks2']))
#         filtered_time = filtered_an.loc[pd.to_datetime(filtered_an['Start_Time'], format='%Y-%m-%d %H:%M:%S.%f') < bin1_start]
#         if filtered_time.empty:
#             # print('empty bin')
#             pel_sums2.append(np.nan)
#         else:
#             pel_sums2.append(sum(filtered_time['Drinks1']+filtered_time['Drinks2']))
#     pel_matrix.append(pel_sums1)
#     pel_matrix.append(pel_sums2)
#     
# bw_matrix1=list(map(list, zip(*bw_matrix)))
# pel_matrix1=list(map(list, zip(*pel_matrix)))
# print(bw_matrix1)
# ax4=fig1.add_subplot(224)
# ax4.set_title(f"B {len(known_tags)}")
# b=len(known_tags)
# for i in range(len(known_tags)):
#     ax4.plot(x , bw_matrix1[i], linestyle='-', marker='o', color=[i/b, 1-i/b, 1-i/b, .5], linewidth=5,label="automated")
# for i in range(len(known_tags)):
#     an_data=[]
#     an_data=data_unit5_coll.loc[data_unit5_coll['Animal'] == known_tags[i]] 
#     an_data.Start_Time=pd.to_datetime(an_data.Start_Time)
#     ax4.plot(an_data.Start_Time, an_data['Weight'] , linestyle='-', marker='o', color=[i/b, 1-i/b, 1-i/b, .9],label="manual")
# for marker_time in marker_times:
#     ax4.axvline(marker_time, color='black', linestyle='dashed')
# # ax4.set_ylabel("weight, g")
# ax4.set_xticks(x)
# ax4.set_xticklabels(x,rotation=30,ha='right')
# fmt=mdates.DateFormatter('%m-%d')
# ax4.xaxis.set_major_formatter(fmt)
# # plt.legend(loc="upper right")
# plt.grid()
# 
# ax3=fig1.add_subplot(222)
# ax3.set_title(f"DROPS")
# # print(len(known_tags))
# for i in range(len(known_tags)):
#     # print(i)
#     # print(pel_matrix1[i])
#     ax3.plot(x , pel_matrix1[i], linestyle='-', marker='o', color=[i/b, 1-i/b, 1-i/b, .5])
# for marker_time in marker_times:
#     ax3.axvline(marker_time, color='black', linestyle='dashed')
# # ax3.set_ylabel("pel")
# ax3.set_xticks(x)
# ax3.set_xticklabels(x,rotation=30,ha='right')
# fmt=mdates.DateFormatter('%m-%d')
# ax3.xaxis.set_major_formatter(fmt)
# ax3.set_ylim([0, 180])
plt.grid()
plt.subplots_adjust(bottom=0.15)
# plt.show()
plt.close()
plt.savefig(loadpath + "flan2_test1.png", bbox_inches='tight', pad_inches=0)
