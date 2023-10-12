# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 23:30:18 2023

@author: augus
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

states = pd.read_csv('Statename.csv')
state_dict = {}
#discarding Washington, D.C. Alaska, Hawaii and Puerto Rico as their data is imcomplete
for index, row in states.iloc[:-4].iterrows():
    code = row['Code']
    name = row['Name']
    state_dict[code] = name

clim_dict = {}
clim_dict['tavg'] = 'Average Temperature'
clim_dict['tmax'] = 'Maximum Temperature'
clim_dict['tmin'] = 'Minimum Temperature'
clim_dict['pcp'] = 'Precipitation'
clim_dict['cdd'] = 'Cooling Degree Days'
clim_dict['hdd'] = 'Heating Degree Days'
clim_dict['zndx'] = 'Palmer Z-Index'

final_climate_data = pd.DataFrame(columns=['State', 'Climate Index', 'Value'])

for state_key, state_name in state_dict.items():
    for clim_key, clim_name in clim_dict.items():
        browser = webdriver.Chrome()

        # Use f-strings to insert state_key and clim_key into the URL
        url = f'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/haywood/{state_key}/{clim_key}/12'
        browser.get(url)

        time.sleep(10)

        page_source = browser.page_source

        browser.quit()

        soup = BeautifulSoup(page_source, 'html.parser')

        datatable = soup.find(id="data-table")

        tbody = datatable.find("tbody", attrs={"aria-live": "polite", "aria-relevant": "all"})
        desired_trs = tbody.find_all("tr", {"class": "endMonth odd", "role": "row"})
        second_tr = desired_trs[1]
        td_elements = second_tr.find_all("td")
        temperature_text = td_elements[1].get_text()
        new_df = pd.DataFrame({'State': state_name, 'Climate Index': clim_name, 'Value': temperature_text}, index = [0])
        final_climate_data = pd.concat([final_climate_data, new_df], ignore_index=True)
        
        
        
        
file_path = 'climate.txt'
final_climate_data.to_csv(file_path, index=False, encoding='utf-8')
