#!/usr/bin/python
'''
saufh.py

MIT License

Copyright (c) 2018 Oriol Sanchez Garcia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 


Readme:
Script to get measurements from the sauter FS series dinamometer. It is posible
to select experiment range, delay between measurements and units.

Instructions:
Lay down the strain gauge in order to get a 0
Start the script to keep the sensor on
Mount the strain gauge in the desired setup
Start recording with the desired timeframe

Changelog:
V0 2018/12/03
 
'''


import serial                         #Serial library, required to comunicate with the cam
import time                           #Time library
import datetime                       #Timestamp library
from datetime import datetime as dtime
import ctypes                         #Conversion Type library
import os
import csv
import sys
#import pandas as pd                   #data manipulation library

#global variables:
homepath='/home/pi/'
units =	{
        3: 'KN',
        4: 'TF',
        5: 'KLBF'
        }
force =	{
        0: 'Press',
        1: 'Pull'
        }
fsign =	{
        0: '-',
        1: '+'
        }
                        
hours = {0:'a', 1:'b',2:'c', 3:'d',4:'e', 5:'f',6:'g', 7:'h',8:'i', 9:'j',10:'k', 11:'l',12:'m', 13:'n',14:'o', 15:'p',16:'q', 17:'r',18:'s', 19:'t', 18:'u',19:'v', 20:'w',21:'x', 22:'y', 23:'z'}

def queryme(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def menu(s,test=False):
        '''
        Configuration Menu, serving as the human input interface
        '''
        num=0
        unit=0
        if test==True: return 60,0
        while not(num in range (1,4)): #1 included, 4 excluded
                if (queryme("Use default time range (1 minute)" )):
                        timed=1*60
                        break 
                else:
                        num=input('Select time frame (1- 10 minutes, 2- 30 minutes, 3 -others): ')
                        if num==1:
                                timed=10*60
                        elif num==2:
                                timed=30*60
                        elif num==3:
                                timed=input('Select time frame in minutes: ')*60
                        print("Selected {} minutes".format(timed/60))
                        if not(queryme("Is this correct?")):num=4 #query again
        selectedOK=True
        while selectedOK==True:
                if (queryme("Use default device resolution?")):
                        resolution=0 
                        break
                else:
                        resolution=input('Select time resolution in seconds: ')
                print("Selected {} seconds".format(resolution))
                if (queryme("Is this correct?")):selectedOK=False #query again
        selectedOK=True
        while selectedOK==True:
                if (queryme("Use default device units? [KN]")):
                        talknerdy(s,'3')
                        unit=3
                        break
                else:
                        while not (unit in range (3,6)):
                                unit=int(input('Select units [KN]=3 [TF]=4 [KLBF]=5:  '))
                                if unit in range (3,6): talknerdy(s,unit) #sets the unit into the device
                                else: print('Please input a valid unit')
                        
                if (queryme("Is this correct?")):selectedOK=False #query again
        return timed, resolution, unit

def init_serial(prt='ttyUSB0', baudrte=9600, timout=1):
        '''
        Defines the default serial port configuration
        '''
        return serial.Serial(
        port='/dev/'+prt,
        baudrate=baudrte,
        timeout=timout,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )


def talknerdy(s,m='9'):
        '''
        s: serial port to talk to
        m: message to send::
                * '2': set the unit to 'zero'
                * '3': use KN units; Kilo Newtons
                * '4': use TF units; Tone Force
                * '5': use KLBF units; Kilo Pound Force
                * '6': set tracking mode on the gauge
                * '7': set peak mode on the gauge
                * '9': Retrieve measurement, default message
        -> The default message is YXXX.XX where Y is the sign and XXX.XX the 
        measurement in the selected units, by default Kilo Newtons
        '''
        s.flushInput()
        s.write(m)
        sign=0
        data=0
        if m=='9':
                read = s.read(7)
                #print(read)
                sign=int(read[0])
                data= round(float(read[1:len(read)]),3)
        time.sleep(.05)
        return sign,data

def storeme(ppath="force"):
        '''
        Checks if a local path exists whithin the home folder, otherwise it creates one.
        Checks if a filename exists within the local path, otherwise creates one.
        '''
        #Folder update
        homep=homepath+ppath #complete path relative to modifiers
        if not (os.path.exists(homep)): os.mkdir(homep)
        #Filename update
        st=dtime.now()
        ffile='FH'+'{0}{1}'.format(st.year,st.timetuple().tm_yday)+hours[st.hour]+'.csv' #FH2018223a.csv
        if os.path.exists(homep+'/'+ffile) == False: #in case file does not exist
                with open(homep+'/'+ffile, 'w') as csvfile:
                        writer=csv.writer(csvfile)
                        writer.writerow(['Timestamp','Sign','Force'])
                        csvfile.close()
        else: print ('File '+ ffile + ' already exists, data will be appended')
        
        return homep,ffile

#Main script
def main():
        debug=False
        #Init the serial port                
        ser=init_serial()
        try: timed,resolution,unit=menu(ser) #timed in minutes, resolution in seconds (0), true for mode Test
        except KeyboardInterrupt:
                print('\rExit                                                            ')                
                exit()
        print (timed,resolution)
        print('Reading data...')
        #talknerdy(ser,'2') #Set the device to '0'  #uncomment for self calibration after deployment.
        #Init recording file
        homep,filename= storeme()
        nowasthen=time.time()
        try:
                while True:
                        #Output message in terminal
                        sign,data=talknerdy(ser) #Parsing default mesage, '9', to read data
                        sys.stdout.write('\rWaiting for user defined start [ctl+C], elapsed time ' +str(round(time.time()-nowasthen))+    '    \r') #Notice that dictionaries are used to parse the unit name and the force direction
                        sys.stdout.flush()
        except KeyboardInterrupt:
                sys.stdout.flush()
                print('\rRecording at file '+filename+'                                                             ')
                pass
        #Init time pointers
        starttime=time.time()
        output=[]
        i=0
        timenow=time.time()-starttime
        try:
                while (timenow)<timed : #Compared against selected timeframe
                        if debug: print('Time since last measurement: ', timenow)
                        #Retrieve the data
                        sign,data=talknerdy(ser) #Parsing default mesage, '9', to read data
                        #Create timestamp
                        st=dtime.now()
                        st='{0}/{1}/{2} {3}:{4}:{5}:{6}'.format(st.year,st.month,st.day,st.hour,st.minute,st.second,st.microsecond)
                        #Create data row
                        output.append([st,fsign[sign],data])
                        #Output message in terminal
                        sys.stdout.write('\r' +force[sign]+' force output '+str(output[i][2])+' '+units[unit] +' remaining time ' +str(round(timed-timenow))+    '    \r') #Notice that dictionaries are used to parse the unit name and the force direction
                        sys.stdout.flush()
                        #Update file
                        with open(homep+'/'+filename, 'ab') as csvfile:
                                writer=csv.writer(csvfile)
                                writer.writerow(output[i])
                                csvfile.close()
                        #Update pointers
                        i+=1
                        time.sleep(resolution)
                        timenow=time.time()-starttime
        except KeyboardInterrupt:
                sys.stdout.flush()
                print('\rFinished reading                                                             ')
                pass       
        ser.close() #Close serial port
        print('\r')
        if debug: print('Total output',output)


if __name__ == "__main__":
    main()

