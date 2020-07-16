#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:32:00 2020

@author: nick
"""

import pandas as pd
import numpy as np

from sys import platform



if platform == "linux" or platform == "linux2":
    data=pd.read_excel("~/Documents/dev/condo_data/condo_data.xlsx")
elif platform == "win32":
    data=pd.read_csv(r"C:\Users\nick\Documents\dev\csv_preprocess\to_downtown_condo\step2_needs_process\toronto_condo_to_process.csv")
  
print(data.head())

# data=data.iloc[1:]

print(data.head())

#remove all rows where price is less than $400,000

print(data[data["PRICE"]>400000])
print(data.head())

data=data[data["PRICE"]>400000].copy()
print('-------------')
#Changing unit numbers to be integer
for i in range(0,len(data['UNIT#'])):
     cell = data.at[i,'UNIT#']
     #cell = cell.upper()
     # print(cell)
     #index=cell.find("PH")
     #if index>=0:
     #    cell=cell[0:index]+"999"+cell[index+2:]
     #index=cell.find('/')
     #if index>=0:
     #    cell=cell[0:index]
     #index=cell.find('\\')
     #if index>=0:
     #    cell=cell[0:index]
     newcell=""
     #for c in cell:
     #    if c.isdigit():
     #        newcell+=c
     #data.at[i, "UNIT#"] = newcell
     print(newcell, i)
print('-------------')

print(data.head())

#Codify the building address
addresses={}
codes=[]
count=1
for i in range(0,len(data['ADDRESS'])):
     cell = str(data.at[i,'ADDRESS'])
     values = cell.split(' ')
     #print(values)
     number=values[0]
     number=number.rjust(10,'0')
     address=" ".join(values[1:])
     #print(address)
     if not address in addresses:
         addresses[address]=count
         count+=1
     code=number+str(count)
     codes.append(code)
print(addresses)
#print(codes)

data['Codes']=np.array(codes)
print(data.head())

# lookup code
code='00000002113'
number=str(int(code[0:10]))
count=code[10:]
count=int(count)

for k,v in addresses.items():
    if v==count:
        address=number+" " + k
print(address)

































