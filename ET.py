# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 11:53:43 2022

@author: ccchen
"""

# The following equation were wrote from "Step by Step Calculation of the 
# Penman-Monteith Evapotranspiration (FAO-56 Method)" UF IFAS Extension
# downloads from https://edis.ifas.ufl.edu/pdf%5CAE%5CAE459%5CAE459-4802269.pdf

import math
PI = 3.1415926

def ET0(Tmax,Tmin,SolRad,WS,RH, LAT, height, JDAY):
    #step1
    Tmean = (Tmax+Tmin)/2
    # Step 2 - solrad 
        #solrad in calculated in MJ/m2/day, no need to convert
    # step 3 - windspeed 
        # 測定高度2公尺，不須轉換
    # step 4 
    X1 = math.exp(17.27*Tmean/(Tmean+237.3))
    X2 = pow(Tmean+237.3, 2)
    VPslope = 4098*0.6108*X1/X2 # slope of saturation vapor pressure
    # Step 5 - Pair (atmospheric pressure)
    X1 = (293-0.0065*height)/293
    Pair = 101.3*pow(X1, 5.26)
    # step 6 - psychrometric constant 乾濕度常數
    psychrom = 1.013e-03 * Pair/(0.622*2.45)
        # 1.013e-3 specific heat at const. pressure (MJ /kg/c)
        # 2.45 latent heat of evaporization MJ/kg
        # 0.622 ratio molecular weight of water vapor 
    # step 7 - delta term
    DT = VPslope/(VPslope + psychrom*(1 + 0.34*WS))
    # step 8 - psi term
    PT = psychrom/(VPslope+psychrom*(1 + 0.34*WS))
    # step 9 - temperature term
    TT = 900/(Tmean + 273)*WS
    # step 10 - saturated vapor pressure
    eTmax = 0.6108 * math.exp(17.27*Tmax/(Tmax+237.3))
    eTmin = 0.6108 * math.exp(17.27*Tmin/(Tmin+237.3))
    es = (eTmax + eTmin)/2 # average saturated vapor pressure
    # step 11 - actual vapor pressure
    ea = es * RH/100
    # step 12 
    # inverse relative distance earth-sun (dr)
    dr = 1 + 0.033 * math.cos(2*PI*JDAY/365)
    # solar declination
    SOLDCLIN = 0.409*math.sin(2*PI*JDAY/365 - 1.39)
    # step 13 - radians of site
    radians = LAT * PI/180
    # step 14 - sunset hour angle
    sunsetAngle = math.acos(-1*math.tan(radians)*math.tan(SOLDCLIN))
    # step 15 - extraterretrial radiation Ra MJ/m2/day
    Gsc = 0.082 # MJ/m2/min solar constant
    X1 = sunsetAngle * math.sin(radians)*math.sin(SOLDCLIN)
    X2 = math.cos(radians)*math.cos(SOLDCLIN)*math.sin(sunsetAngle)
    Ra = 24*60/PI * Gsc * dr * (X1 + X2)
    # step 16 - clear sky solar radiation (Rso)
    Rso = (0.75 + 2.0e-5 * height)*Ra
    # step 17 - net shortwave radiation (Rns)
    albedo = 0.23 # albedo for hypothetical grass
    Rns = (1-albedo)*SolRad
    # step 18 - net outgoing long wave solar radiation (Rnl)
    k_bolzmann = 4.903e-09
    X1 =(pow(Tmax+273.16, 4) + pow(Tmin+273.16,4))/2
    X2 = 0.34- 0.14*pow(ea,0.5)
    X3 = 1.35*SolRad/Rso - 0.35
    Rnl = k_bolzmann * X1 * X2 * X3
    # step 19 - net radiation (Rn)
    Rn = Rns - Rnl
    Rng = 0.408 * Rn
    # final step - put it together
    ET0 = DT * Rng + PT * TT * (es-ea)
    return ET0

if __name__ == "__main__" : 

    test = ET0(Tmax=30, Tmin=16, SolRad = 24, WS=3, RH=80, LAT=24.1, height=80, JDAY=40)
    print(test)

    
    
    