#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:32:00 2020
 
@author: nick
"""
 
import pandas as pd
import numpy as np
 
from sys import platform
 
data=pd.read_excel("condo_data_v2.xlsx")

 
#if platform == "linux" or platform == "linux2":
#    data=pd.read_excel("~/Documents/dev/aws_deepar_condo/condo_data.xlsx")
#elif platform == "win32":
#    data=pd.read_csv(r"C:\Users\nick\Documents\dev\csv_preprocess\to_downtown_condo\step2_needs_process\toronto_condo_to_process.csv")
    
 
print(data.head())
 
#remove all rows where price is less than $400,000
data=data[data["PRICE"]>400000].reset_index(drop=True)



print(data.head())
print('------------------------------')
 
#Changing unit numbers to be integer
for i in range(0,len(data['UNIT#'])):
     cell = str(data.at[i,'UNIT#'])
     cell = cell.upper()
     # print(cell)
     index=cell.find(" ")
     if index>=0:
         cell='NaN'
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
 
 
#Convert SQFT column to integer
for i in range(0,len(data['SQFT'])):
     cell = str(data.at[i,'SQFT'])
     values = cell.split('-')
     median = 0
     if(len(values) == 2):
         median = int((int(values[0]) + int(values[1]))/2)
         if median == 249:
             median = 400
     data.at[i,'SQFT'] = median
 
data['SQFT']=data['SQFT'].astype('int64')
 
print(data.head())
print(data["SQFT"])
print(data["PRICE"])
 
 
#Convert date and set each day to 01
 
for d in range(0,len(data['DATE'])):
     cell = data.at[d,'DATE']
      
     cell=cell.replace(day=1)
     data.at[d, 'DATE'] = cell
          
print('-------------')
print(data["DATE"])
 
 
#Codify the building address
addresses={}
codes=[]
count=1
for i in range(0,len(data['ADDRESS'])):
     cell = str(data.at[i,'ADDRESS'])
     values = cell.split()
     #print(values)
     number=values[0]
     number=number.rjust(10,'0')
     address=" ".join(values[1:])
     if not address in addresses:
         addresses[address]=count
         count+=1
     else:
         count = addresses[address]
     #print(address,count)
     code=number+str(count)
     codes.append(code)
      
# print lookup dictionary      
#print(addresses)
#print(codes)
 
# mak column of address codes
data['Codes']=codes
 
print(data.head())
 
data["PARK"].fillna(0, inplace=True)
 
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
 
 
     
# test code lookup
# lookup code
code='00000002113'
address = code_to_address(code,addresses)
print(code, "=", address)
code = address_to_code(address, addresses)
print(address, "=", code)
 
#   Print JSON File according to specs found at "https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html'
 
#   {"start": "1999-01-30 00:00:00", "target": [2.0, 1.0], "cat": [1, 4], "dynamic_feat": [[1.3, 0.4]]}
#   {"start": "2020-01-01 00:00:00", "target": [1500000, NaN, NaN, NaN], "cat":[codes], "dynamic_feat": [[SQFT, beds, baths, parking, unit#]]}
# data.to_json(r'condo_data.json', date_format='iso')
#{"start": 2018-01-01 00:00:00, "target": [490000, 520000], "cat": 00000000111,"dynamic_feat": [[400,1.0, 1, 0.0, ]]}

# sort by date
data.sort_values(by='DATE',inplace=True)

duplicated_series = data.duplicated(['UNIT#', 'Codes'])
 
duplicate_data=data[duplicated_series]
                                     
duplicate_data.to_csv('duplicate.csv')
duplicate_data['FOUND'] = 0

                                     
#duplicate_data.sort_values(by='DATE',inplace=True)
#group_data=data.groupby(['UNIT#', 'Codes'])
                         
#for key, item in group_data:
#    print(group_data.get_group(key), "\n\n")
                             
#for g in group_data.groups:
#    print('group')
#    print(g)
#duplicate_data['FOUND'] = 0

#duplicate_indexes = duplicate_data.index

from datetime import datetime,timedelta

f=open('condo_data.json', 'w')

for index, row in duplicate_data.iterrows():
    
    
    # get unit and codes
    unit = row['UNIT#']
    codes = row['Codes']
    

    # get duplicaes for this entry
    group_data = data[(data['UNIT#']==unit) &  (data['Codes']==codes)]   
                                     
    print(group_data);
    
    # for each entry in group
    first = True
    for index2, row2 in group_data.iterrows():
        
        
        if first:
            
            first = False
            start_date = row2['DATE']
    
            year = start_date.year
            month = start_date.month
            end_date = datetime.today()
            
            current = datetime(year, month, 1)
    
           
            f.write('{"start": '+'"'+str(row2['DATE'])+ '", '+ '"target": ['+ str(row2['PRICE'])+',')
            
            month = ((month + 1) % 12) or 12
            if month == 1:
                year += 1
    
           
        else:
            
            group_date = row2['DATE']
             
            while(True):
        
                current = datetime(year, month, 1)
        
                if current.month == end_date.month and current.year == end_date.year:
                    break
                
                else:
            
                    if month == group_date.month and year == group_date.year:
                        f.write(' '+str(row['PRICE'])+',')
                        
                        month = ((month + 1) % 12) or 12
                        if month == 1:
                            year += 1
                        break;
                        
                    else:
                        f.write(' "NaN",')
                
                month = ((month + 1) % 12) or 12
                if month == 1:
                    year += 1

           
       # for all months
    while True:
        current = datetime(year, month, 1)
        if current.month == end_date.month and current.year == end_date.year:
            break
        else:
            f.write(' "NaN",')
            month = ((month + 1) % 12) or 12
            if month == 1:
                year += 1
    
    f.write(' "NaN"') # last one
    f.write('], '+'"cat": '+'['+str(row['Codes']) + '],')
    f.write(' "dynamic_feat": ' + '[['+str(row['SQFT'])+',' + str(row['BEDS']))
    f.write(', '+str(row['BATH'])+', '+str(row['PARK'])+', '+ str(row['UNIT#'])+']]}\n')
    


# remove all duplicates   

duplicate_data=data.duplicated(['UNIT#', 'Codes'],keep = False)

# passing NOT of bool series to see unique values only 
data = data[~duplicate_data] 

#/////////////////////////////////////////////////////////////////////////////

 
#duplicates need to be combined with right date and Nan
 
for index, row in data.iterrows():
    f.write('{"start": '+'"'+str(row['DATE'])+ '", '+ '"target": '+ '['+str(row['PRICE'])+', ')
    
    
    # if this index is a duplicate
             
    # write out NAN'S    
    start_date = row['DATE'];
    
    year = start_date.year
    month = start_date.month
    end_date = datetime.today()
    
    # for all months
    while True:
        current = datetime(year, month, 1)
        if current.month == end_date.month and current.year == end_date.year:
            break
        else:
            f.write(' "NaN",')
            month = ((month + 1) % 12) or 12
            if month == 1:
                year += 1
    
    f.write(' "NaN"') # last one
    f.write('], '+'"cat": '+'['+str(row['Codes'])+']' + ',')
    f.write('"dynamic_feat": ' + '[['+str(row['SQFT'])+',' + str(row['BEDS']))
    f.write(', '+str(row['BATH'])+', '+str(row['PARK'])+', '+ str(row['UNIT#'])+']]}\n')
f.close() 

print("json written to file: condo_data.json" )