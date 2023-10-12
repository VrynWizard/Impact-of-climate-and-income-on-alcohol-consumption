# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd

#Get Series id and States From api(each Series id represents a state's yearly data from 1984 to 2022),
#Then add Series id and States to two seperate lists.

headers = {'Content-Type': 'application/json'}
url0= 'https://api.stlouisfed.org/fred/release/tables?release_id=249&api_key=16716e12f444721cd3031185e241a671&element_id=259515&file_type=json'
response0 = requests.get(url0, headers = headers)
series_id = json.loads(response0.content.decode('utf-8'))
idlist=[]
namelist=[]
for i in series_id['elements']:
    idlist.append(series_id['elements'][i]['series_id'])
    namelist.append(series_id['elements'][i]['name'])

#Get 2021 income data from each Series id, then add the data to a list(valuelist)
valuelist=[]
for j in idlist:
    url1='https://api.stlouisfed.org/fred/series/observations?series_id=%s&api_key=16716e12f444721cd3031185e241a671&file_type=json' %j
    response1 = requests.get(url1, headers = headers)
    data = json.loads(response1.content.decode('utf-8'))
    data_2021=data['observations'][-2]['value']
    valuelist.append(data_2021)

#Combine two lists together as a dataframe
income_data=pd.DataFrame({'State':namelist,'Value': valuelist})
print(income_data)

#Write the income_data to a csv
income_data.to_csv('Real Median Household Income by State.csv', index=False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    