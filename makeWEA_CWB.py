# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:00:54 2022

@author: ccchen
"""
import csv
from datetime import datetime
import Weather

CWBfilename = "CWBfile/G2F820_daily_2000-2020.csv"
LAT = 24.00
LON = 120.50
YEAR = 2020
ELEV = 80
Tmax_lst = []
Tmin_lst = []
SolRad_lst = []
Precp_lst = []





def findIndex(inputList,term):    
    for i, j in enumerate(inputList):
        if j == term:
            return i # end of the function


counter = 0
yearOld = 1970

csvwrite = open("TARI.wea","w",newline='') 
writer = csv.writer(csvwrite, quoting=csv.QUOTE_NONNUMERIC, delimiter=' ')
header = ["JDAY", "DATE", "SRAD","TMAX", "TMIN", "RAIN", "WIND", "RH"]
writer.writerow(header)

with open( CWBfilename,newline='') as batchfile:
    rows = csv.reader(batchfile)
    next(rows) # read the title out 
    header = next(rows)
    # find index of specific item
    indexDate = findIndex(header, '觀測時間')
    indexTmax = findIndex(header,'最高氣溫(℃)')
    indexTmin = findIndex(header, '最低氣溫(℃)')
    indexWs = findIndex(header,'平均風速(m/s)')
    indexRain = findIndex(header,'累計雨量(mm)')
    indexRh = findIndex(header,'平均相對溼度( %)')
    indexSrad = findIndex(header,'累積日射量(MJ/m2)')
    # read item from each row
    for row in rows:
        # read date
        datestr = row[indexDate]
        date = datetime.strptime(datestr,"%Y-%m-%d")
        datestr = date.strftime("%m/%d/%Y")
        datestr = "%s"%datestr
        #datestr = f"{datestr}"
        doy = date.timetuple().tm_yday
        loc = doy - 1
        year = date.year
        
        # read grid weather file
        if year != yearOld:
            Tmax_lst = Weather.readValue(LON, LAT, year, "最高溫")
            Tmin_lst = Weather.readValue(LON, LAT, year, "最低溫")
            srad_lst = Weather.readValue(LON, LAT, year, "日射量")
            precp_lst = Weather.readValue(LON, LAT, year, "降雨量")
            RH_lst = Weather.readValue(LON,LAT,year,"相對濕度")
            WS_lst = Weather.readValue(LON,LAT,year,"平均風速")
            yearOld = year
            
        if len(row[indexTmax]) > 0:
            tmax = float(row[indexTmax])
        else:
            tmax = Tmax_lst[loc]
            
        if len(row[indexTmin])>0:
            tmin = float(row[indexTmin])
        else:
            tmin = Tmin_lst[loc]
            
        if len(row[indexWs])>0:
            ws = float(row[indexWs])
        else:
            ws = WS_lst[loc]
            
        if len(row[indexRain])>0:
            rain = float(row[indexRain])
        else:
            rain = precp_lst[loc]
        
        if len(row[indexRh])>0:
            rh = int(row[indexRh])
        else:
            rh = RH_lst[loc]
        if len(row[indexSrad])>0:
            srad = float(row[indexSrad])
        else:
            srad = srad_lst[loc]
        #srad = round(srad,2)
        srad = float("{:.3f}".format(srad))
        #srad = "{:.2f}".format(srad)
        #srad = format(srad, ".2f")
        
        # write table
        toWrite = [doy, datestr, srad, tmax, tmin, rain, ws, rh]
        writer.writerow(toWrite)
        print(toWrite)
        
csvwrite.close() 
    
if __name__ == "__main__" :
    L1 = ['foo', 'bar', 'baz']
    print(findIndex(L1,"bar"))
    