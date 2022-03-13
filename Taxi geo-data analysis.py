#!/usr/bin/env python
# coding: utf-8

# In[8]:


# read Taxi daa file 
import csv


# In[1]:


def read_CSV_data(filename, data = []):
    file = open(filename)# read files 
    csvreader = csv.reader(file)
    for row in csvreader:
        data.append(row)
    file.close()
    return data  # data is 2D list 


# In[ ]:


# for generate the coordinate of the files 
import random
def append_data (fileName, outbutfileName):
    with open(fileName,'r') as csvinput:
        with open(outbutfileName, 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            
            for row in csv.reader(csvinput):
                if row[17] == "congestion_surcharge":  # 17 is the number of the last row in
                    writer.writerow(row+["Longitude", "Latitude"])
                    print(row+["Longitude", "Latitude"])
                else: 
                    long = random.uniform(-74.25909, -73.70001)
                    lat = random.uniform(40.47740, 40.91758)
                    writer.writerow(row+[str(long),str(lat)])
    fileName.close()
    outbutfileName.close()


# In[ ]:


for i in range (1, 6):
    append_data("2021_0"+str(i)+".csv","2021_1"+str(i)+".csv")


# In[2]:


# import needed library 
import pandas as pd
from folium import Map
from folium.plugins import HeatMap
from datetime import datetime, timedelta # for second part of the code for make opperation on the time value


# In[3]:


df = pd.read_csv('2021_01.csv')
#print(df["Longitude"].tolist(),4)


# In[4]:


#create heat map 
for_map = Map(location=[40.730610, -73.935242], zoom_start=9 )
hm_wide = HeatMap(
    list(zip(df.Latitude.values, df.Longitude.values)),
    min_opacity=0.2,
    radius=17, 
    blur=15, 
    max_zoom=1,
)


# In[5]:


for_map.add_child(hm_wide)
# show data with out any filter so in this way we got unmeaning full data


# In[6]:


inputdate = input("please enter the date in format: DD/MM/YY  ")
inputhour = input("Please enter the hour in format: HH:MM  ")


# In[9]:


date = inputdate.split("/") # data typ list YY MM DD items type is string 
csvFileData = read_CSV_data(filename = "2021_"+date[1]+".csv" )


# In[10]:


# in this part of the code we are try to get the the heat map for the 
# given date and hour for getting more unstandabile data 
heatmapListLat = [] # keep the coordinate of the given date 
heatmapListLong = [] # keep the coordinate of the given date 
time_limit = 30
inputTime = datetime.strptime(inputhour, '%H:%M') # giving the time limit for the given date
lower_limit = (inputTime - timedelta(minutes = time_limit)).strftime("%H:%M")
bigger_limit = (inputTime + timedelta(minutes = time_limit)).strftime("%H:%M")
for i in range(1, len(csvFileData)):  # tpep_pickup_datetime = [1], Longitude [18], Latitude [19]
    if len(csvFileData[i]) != 0: # because we have empty row
        #print(i)
        CSV_data = csvFileData[i][1] .split(" ")
        CSVdate = CSV_data[0].split("-")
        CSV_time = CSV_data[1]
        #print(CSV_time, CSVdate, time)
        if date[2] == CSVdate[0] and date[1] == CSVdate[1] and date[0] == CSVdate[2]:
            #print("hello their", lower_limit, CSV_time, bigger_limit, lower_limit <= CSV_time <= bigger_limit)
            if lower_limit <= CSV_time <= bigger_limit:
                heatmapListLat.append(csvFileData[i][19])
                heatmapListLong.append(csvFileData[i][18])
                #print("date appended")

            
new_hm_wide = HeatMap(
    list(zip(heatmapListLat, heatmapListLong)),
    min_opacity=0.2,
    radius=17, 
    blur=15, 
    max_zoom=1,
)


# In[11]:


second_map = Map(location=[40.730610, -73.935242], zoom_start=9 )
second_map.add_child(new_hm_wide)


# In[ ]:




