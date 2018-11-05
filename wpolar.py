# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 12:42:32 2018
Polar plot of relative thrust due to wind dir/speed being the wind dir referenced to the ship roll axis 
@author: oriol sanchez garcia
@license MIT
"""
import numpy as np
import matplotlib.pyplot as plt


def mapr(r):
   """Remap the radial axis."""
   return 90 - r


r = np.arange(0, 2, 0.01)
theta = 1/2 * np.pi * r

#r = np.arange(0, 90, 0.01)
#theta = 2 * np.pi * r / 90
#
#ax.plot(theta, mapr(r))
#ax.set_yticks(range(0, 90, 10))                   # Define the yticks
#ax.set_yticklabels(map(str, range(90, 0, -10)))   # Change the labels

#pure Numpy CSV read
pdata=np.loadtxt(open("wtest.csv", "rb"), delimiter=";", skiprows=1)
r=pdata[:,0]/(np.pi*18)

#print(pdata[:,0)]) #Axis in Degrees
#print(pdata[:,1]) #8knot
#print(pdata[:,2]) #12knot
#print(pdata[:,3]) #16knot
#print(pdata[:,4]) #20knot


#ax = plt.subplot(111, projection='polar')


#cmap='viridis' #additional colorset maps

fig = plt.figure()
ax = fig.add_subplot(111, polar=True,facecolor='white')
ax.set_xticks(np.pi/180. * np.linspace(0,  180, 18, endpoint=False))
ax.set_thetamin(0)
ax.set_thetamax(180)

#ax.plot(pdata[:,1], r)
c = ax.scatter(r, pdata[:,1], c=pdata[:,1], s=5, cmap='viridis',alpha=0.75, label="8kt")
#c = ax.scatter(-r, pdata[:,1], c=pdata[:,1], s=5, cmap='viridis',alpha=0.75, label="8kt")
d = ax.scatter(r, pdata[:,2], c=pdata[:,2], s=5, cmap='Blues', alpha=0.75, label="12kt")
#d = ax.scatter(-r, pdata[:,2], c=pdata[:,2], s=5, cmap='Blues', alpha=0.75, label="12kt")
e = ax.scatter(r, pdata[:,3], c=pdata[:,3], s=5, cmap='Greens', alpha=0.75, label="16kt")
#e = ax.scatter(-r, pdata[:,3], c=pdata[:,3], s=5, cmap='Greens', alpha=0.75, label="16kt")
f = ax.scatter(r, pdata[:,4], c=pdata[:,4], s=5, cmap='Oranges', alpha=0.75, label="20kt")
#f = ax.scatter(-r, pdata[:,4], c=pdata[:,4], s=5, cmap='Oranges', alpha=0.75, label="20kt")


ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5),fancybox=True) #Mover leyenda a la derecha



#ax.plot(pdata[:,4], pdata[:,0])

plt.show()