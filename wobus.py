# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 10:34:47 2018
Herman Wobus air density equations
@author: oriol sanchez garcia
@license MIT
"""
#import numpy
import math as m

def get_frost_point_c(t_air_c, dew_point_c):
    """Compute the frost point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param dew_point_c: current dew point in degrees Celsius
    :type dew_point_c: float
    :return: the frost point in degrees Celsius
    :rtype: float
    """
    dew_point_k = 273.15 + dew_point_c
    t_air_k = 273.15 + t_air_c
    frost_point_k = dew_point_k - t_air_k + 2671.02 / ((2954.61 / t_air_k) + 2.193665 * m.log(t_air_k) - 13.3448)
    return frost_point_k - 273.15

def get_dew_point_c(t_air_c, rel_humidity):
    """Compute the dew point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param rel_humidity: relative humidity in %
    :type rel_humidity: float
    :return: the dew point in degrees Celsius
    :rtype: float
    """
    A = 17.27
    B = 237.7
    alpha = ((A * t_air_c) / (B + t_air_c)) + m.log(rel_humidity/100.0)
    return (B * alpha) / (A - alpha)

def air_density1(t_air,P_air,Td,Rv=461.495,Rd=287.058,eso=6.1078, debug=False):
    """Compute the air density in kg/m3 with the first approach
    Td: dew temperature in degrees Celsius
    t_air_c: current ambient temperature in degrees Celsius
    Rv: Water Vapour Specific gas constant in J/(Kg*K)
    Rd: Dry Air Specific gas constant in J/(Kg*K)
    P_air: Air pressure in hPa
    rel_humidity: relative humidity in %
    returns air_density in kg/m3
    """
    #Constants
    c0 = 0.99999683
    c1 = -0.90826951e-2
    c2 = 0.78736169e-4
    c3 = -0.61117958e-6
    c4 = 0.43884187e-8
    c5 = -0.29883885e-10
    c6 = 0.21874425e-12
    c7 = -0.17892321e-14
    c8 = 0.11112018e-16
    c9 = -0.30994571e-19 
    if debug: print("\nMethod 1: with dew temperature")
    #Pressure of Water Vapor
    p = c0+Td*(c1+Td*(c2+Td*(c3+Td*(c4+Td*(c5+Td*(c6+Td*(c7+Td*(c8+Td*c9))))))))
    if debug: print("Partial vapour pressure:",p)
    Es=eso/p**8 #(hPa)
    Pv=Es # at Tdewpoint   #(hPa)
    if debug: print("Water vapour pressure:",Pv, "hPa")
    #Pressure of Dry Air (hPa)
    Pd=P-Pv
    if debug: print("Dry air pressure:",Pd, "hPa")
    #Air density (kg/m3)
    Rho=(Pd/(Rd*(t_air+273))+Pv/(Rv*(t_air+273)))*100
    print("Rho:",Rho, "kg/m3")

def air_density2(t_air,P_air,Td,rel_humidity,Rv=461.495,Rd=287.058,eso=6.1078, debug=False):
    """Compute the air density in kg/m3 with the first approach
    Td: dew temperature in degrees Celsius
    t_air_c: current ambient temperature in degrees Celsius
    Rv: Water Vapour Specific gas constant in J/(Kg*K)
    Rd: Dry Air Specific gas constant in J/(Kg*K)
    P_air: Air pressure in hPa
    rel_humidity: relative humidity in %
    returns air_density in kg/m3
    """
    if debug: print("\nMethod 2: with dew temperature and relative humidity")
    p1=eso*10**(7.5*Td/(Td+237.3))
    pv1=p1*rel_humidity/100
    pd1=P-pv1
    if debug: print("Water vapour pressure 2:",pv1, "hPa")
    if debug: print("Dry air pressure 2:",pd1, "hPa")
    Rho=(pd1/(Rd*(t_air+273))+pv1/(Rv*(t_air+273)))*100
    print("Rho 2:",Rho, "kg/m3")

if __name__ == "__main__":
   # execute only if run as a script   
    debug=True
    #Data from sensors
    T=15
    P=1013.25
    RH=60.86    
    Td=(get_dew_point_c(T, RH))
    air_density1(T,P,Td,debug=debug)  
    air_density2(T,P,Td,RH,debug=debug)  
