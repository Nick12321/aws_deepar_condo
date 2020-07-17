

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:32:00 2020

@author: nick
"""

import pandas as pd
import numpy as np

from sys import platform

#data=pd.read_excel("condo_data.xlsx")

if platform == "linux" or platform == "linux2":
    data=pd.read_excel("~/Documents/dev/condo_data/condo_data.xlsx")
elif platform == "win32":
    data=pd.read_csv(r"C:\Users\nick\Documents\dev\csv_preprocess\to_downtown_condo\step2_needs_process\toronto_condo_to_process.csv")
 
print(data.head())

#remove all rows where price is less than $400,000
data=data[data["PRICE"]>400000].reset_index(drop=True)

print(data.head())


#print('-------------')
#Changing unit numbers to be integer
for i in range(0,len(data['UNIT#'])):
     cell = str(data.at[i,'UNIT#'])
     cell = cell.upper()
     # print(cell)
     index=cell.find("PH")
     if index>=0:
         cell=cell[0:index]+"999"+cell[index+2:]
     index=cell.find('/')
     if index>=0:
         cell=cell[0:index]
     index=cell.find('\\')
     if index>=0:
         cell=cell[0:index]
     newcell=""
     for c in cell:
         if c.isdigit():
             newcell+=c
     data.at[i, "UNIT#"] = newcell
     #print(newcell, i)

#print('-------------')

#print(data.head())


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
     
# print lookup dictionary     
#print(addresses)
#print(codes)

# mak column of address codes
data['Codes']=codes

print(data.head())


# return address for code
def code_to_address(code,addresses):
    number=str(int(code[0:10]))
    count=code[10:]
    count=int(count)
    address = ""
    for k,v in addresses.items():
        if v==count:
            address=number+" " + k
    return address


# return code for address
def address_to_code(address, addresses):
    
     values = address.split(' ')
     #print(values)
     number=values[0]
     number=number.rjust(10,'0')
     address=" ".join(values[1:])
     
     if(address in addresses):
         code = addresses[address]
         number = number + str(code)
         return number
     
     else:
        return "000000000"


    
# test code loolup
# lookup code
code='00000002113'
address = code_to_address(code,addresses)

print(code, "=", address)

code = address_to_code(address, addresses)
    
print(address, "=", code)

