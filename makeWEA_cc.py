# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 08:37:05 2022

@author: ccchen
"""
from datetime import datetime
from datetime import timedelta
import HourWea
import csv

def DOY2DATE(year1,jday):
    if jday > 365:
        year = int(year1)+1
        DOY = jday - 365

    else:
        year = int(year1)
        DOY = jday 

    nonLeap = {1:0,2:31,3:59,4:90,5:120,6:151,7:181,8:212,9:243,
               10:273,11:304,12:334}
    for i in range(1,12+1):
        if DOY > nonLeap[i]:
            month = i
            day = DOY-nonLeap[i]

    toReturn = "%02d/%02d/%d"%(month,day,year)
    return toReturn # end of the function

def findLocation(idValue):
    filename = "G:/TCCIP WEA/臺灣歷史氣候重建資料_5km/grid_5km_town2.csv"
    with open(filename, newline='') as readfile:
        grids = csv.reader(readfile, delimiter = ',')
        next(grids)
        for grid in grids:
            if int(grid[0]) == idValue:
                return grid
                break

            



def runOneGrid(idValue,yearStart, yearEnd,rcp,model):
    grd = findLocation(idValue)
    ID = int(grd[0])
    LON = float(grd[1])
    LAT = float(grd[2])
    site = grd[3]
    
    header = ["JDAY","DATE","SRAD","TMAX","TMIN","RAIN","WIND","RH"]
    #header =  ["JDAY","DATE","SRAD","TMAX","TMIN","RAIN"]
    # create csv and write header
    filename = "wea file/grd%d_%s_%s.csv"%(idValue,rcp,model)
    csvwrite = open(filename,'w',newline='') 
    writer = csv.writer(csvwrite,delimiter=',')

    writer.writerow(header)

    # read weather data the grid, actually it read weather file in two years
    for year in range(yearStart,yearEnd):
        # create class    
        Wea = HourWea.ReadWea(year)
        Wea.futureWea(LON, LAT, site,rcp,model)
        tmaxLst = Wea.Tmax  
        tminLst = Wea.Tmin
        solRadLst = Wea.SolRad
        rainLst = Wea.Rain
        rhLst = Wea.rh
        wsLst = Wea.windSpeed
        
        # DOY
        DOY = 1
        counter = 0
        for d in range(len(tmaxLst)):
            datastr = DOY2DATE(year,DOY)
            datestr = "'%s'"%datastr
            srad = solRadLst[counter]
            tmax = tmaxLst[counter]
            tmin = tminLst[counter]
            rain = rainLst[counter]
            rh = rhLst[counter]
            ws = wsLst[counter]
            toWrite = [DOY,datestr,round(srad,2),round(tmax,1),round(tmin,1),round(rain,1),
                       round(ws,1),round(rh,0)]
            writer.writerow(toWrite)
            print(toWrite)
                        
            
            counter += 1
            DOY += 1
        
    csvwrite.close()
if __name__ == "__main__" :
    
    # runOneGrid(235,2030,2051,"rcp45","bcc-csm1-1")
    # runOneGrid(258,2030,2051,"rcp45","bcc-csm1-1")
    # runOneGrid(279,2030,2051,"rcp45","bcc-csm1-1")
    # runOneGrid(280,2030,2051,"rcp45","bcc-csm1-1")
    # runOneGrid(306,2030,2051,"rcp45","bcc-csm1-1")
    # runOneGrid(307,2030,2051,"rcp45","bcc-csm1-1")
    # runOneGrid(308,2030,2051,"rcp45","bcc-csm1-1")
    # runOneGrid(337,2030,2051,"rcp45","bcc-csm1-1")
    test = findLocation(235)
    print(test)

