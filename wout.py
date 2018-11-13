# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:02:36 2018

@author: oriol
"""

import wobus as wb

class naca4():
    '''
    At some point in the future the naca4() class will automatically calculate its cl, cd 
    for a given profile acording to the naca 4 code classification rules: NACA MPXX 
        M is the maximum camber divided by 100. In the example M=2 so the camber is 0.02 or 2% of the chord
        P is the position of the maximum camber divided by 10. In the example P=4 so the maximum camber is at 0.4 or 40% of the chord.
        XX is the thickness divided by 100. In the example XX=12 so the thiickness is 0.12 or 12% of the chord.
    '''
    def __init__(self, profile,temperature=25, density=1, pressure=1):
        if profile=='0017':
            self.profile='0017'
            self.cl = {'0' : 0.00, '0.5' : 0.04}
            self.cd = {'0' : 0.009, '0.5' : 0.009}
            self.temperature=temperature
            self.density=density
            self.pressure=pressure
            
        if profile=='0025':
            #From SANDIA Labs report
            self.profile='0025'
            self.cl = {'0':0.00,'1':0.11,'2':0.22,'3':0.33,'4':0.41,'5':0.51,'6':0.61,'7':0.70,'8':0.79,'9':0.87,
                       '10':0.95,'11':1.02,'12':1.08,'13':1.13,'14':1.17,'15':1.21,'16':1.24,'17':1.26,'18':1.28,'19':1.30,
                       '20':1.31,'21':1.33,'22':1.34,'23':1.36,'24':1.37,'25':1.40,'26':1.42,'27':1.44,'30':0.59,'35':0.95,
                       '40':1.04,'45':1.05,'50':1.02,'55':0.96,'60':0.88,'65':0.76,'70':0.63,'75':0.50,'80':0.37,'85':0.23,
                       '90':0.09,'95':-0.16,'100':-0.19}
            self.cd = {'0':0.008,'1':0.008,'2':0.009,'3':0.009,'4':0.009,'5':0.009,'6':0.010,'7':0.010,'8':0.011,'9':0.012,
                       '10':0.013,'11':0.014,'12':0.015,'13':0.016,'14':0.018,'15':0.019,'16':0.021,'17':0.026,'18':0.025,'19':0.027,
                       '20':0.029,'21':0.032,'22':0.034,'23':0.037,'24':0.040,'25':0.044,'26':0.047,'27':0.051,'30':0.570,'35':0.745,
                       '40':0.920,'45':1.075,'50':1.215,'55':1.345,'60':1.470,'65':1.575,'70':1.665,'75':1.735,'80':1.780,'85':1.800,
                       '90':1.800,'95':1.780,'100':1.750}
            self.temperature=temperature
            self.density=density
            self.pressure=pressure
            
        



#### MAIN PROGRAM FOR TEST.   
if __name__ == '__main__':

    debug=True
    #Data from sensors
    T=15
    P=1013.25
    RH=60.86    
    
    #Dew temperature
    Td=(wb.get_dew_point_c(T, RH,debug)) 
    #Frost temperature
    Tf=(wb.get_frost_point_c(T, Td,debug)) 
    #Air density ----- Using wobus method
    rho=wb.air_density1(T,P,Td,debug=debug)    
    
    wing=naca4('0025')
    print('Naca profile',wing.profile)
    print('  Cl')
    for key, value in (wing.cl.items()):
        print('    ',key, value)
        
    print('  Cd')
    for key, value in (wing.cd.items()):
        print('    ',key, value)