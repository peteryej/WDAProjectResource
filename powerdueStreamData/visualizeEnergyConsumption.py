#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys,os,argparse
from IPython.display import HTML


# In[2]:



path = '/home/wdauser/Desktop/testOutput/'

fileName = 'test0.csv'  
print('input file: '+fileName)

df = pd.read_csv(path+fileName, skiprows=1, names=['time (s)', 'ch0 Radios(V)', 'ch1 Actuators(V)', 'ch2 Sensors(V)', 'ch3 Processor(V)'])


#df.head(10)


# In[3]:



def plotTimeRange(a=0, b=25):
    secondRange = df.shape[0]/25
    
    plt.figure()
    df.iloc[a*secondRange:b*secondRange,:].plot(x='time (s)', y=['ch1 Actuators(V)', 'ch2 Sensors(V)', 'ch3 Processor(V)'], subplots=True, figsize=(10,10))

plotTimeRange(0,25)


# In[4]:




def calcEnergy(colName):
    r = .4
    totalRaw = (df[colName].sum())*3.3/25/r
    
    if colName.find('cessor') >=0:
        r = 1.33  
        totalRaw = (df[df[colName]>.1].sum()[colName])*3.3/25/r
    
    delta = df['time (s)'].iloc[-1]/df.shape[0]
    energy = totalRaw*delta   
    print("{0:.5f} J".format(energy))
    return energy
    


# In[5]:


processorEnergy = calcEnergy('ch3 Processor(V)')


# In[6]:


radioEnergy = calcEnergy('ch2 Sensors(V)')


# In[7]:


totalEnergy = processorEnergy + radioEnergy

print('total energy {0:.5f} J'.format(totalEnergy))


# In[ ]:




