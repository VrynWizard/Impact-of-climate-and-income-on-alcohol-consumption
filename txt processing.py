# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 18:54:32 2023

@author: chenkai3
"""

import pandas as pd

column_widths = [4, 3, 2, 11, 10, 11, 6, 3, 11, 6, 3, 2, 4, 10]
US_alcohol = pd.read_fwf("niaaa.nih.gov_sites_default_files_pcyr1970-2021.txt", widths=column_widths, header=None, na_values='.', skiprows = 128)

US_alcohol.columns = ['Year', 'State', 'Beverage Type', 'Beverage Gallon', 'Ethanol Gallon', 'Population(>14)', 'Average(>14)', 'Decile(>14)', 'Population(>21)', 'Average(>21)', 'Decile(>21)', 'Source', 'ABV', 'Ethanol by ABV']

US_alcohol = US_alcohol.applymap(lambda x: x.strip() if isinstance(x, str) else x)

lines = open("niaaa.nih.gov_sites_default_files_pcyr1970-2021.txt").readlines()[56:107]

id_statename = pd.DataFrame(columns=['ID', 'StateName'])

# Extract ID and StateName from text data
for line in lines:
    line = line.strip()  # Remove leading/trailing whitespace
    parts = line.split()
    newline = pd.DataFrame({'ID': int(parts[0]), 'StateName': parts[1]}, index = [0])
    id_statename = pd.concat([id_statename, newline], ignore_index=True)

additional_records = pd.DataFrame({
    'ID': [91, 92, 93, 94, 99],
    'StateName': ["Northeast Region", "Midwest Region", "South Region", "West Region", "United States"]
})

id_statename = pd.concat([id_statename, additional_records],ignore_index=True)


US_alcohol = pd.merge(US_alcohol, id_statename, left_on='State', right_on='ID', how='left')

US_alcohol['Beverage Type'] = US_alcohol['Beverage Type'].replace({
    1: 'Spirits',
    2: 'Wine',
    3: 'Beer',
    4: 'All Beverages'
})

US_alcohol.drop(['ID', 'State'], axis=1, inplace=True)

US_alcohol.rename(columns={'StateName': 'State'}, inplace=True)

US_alcohol = US_alcohol[['Year', 'State'] + [col for col in US_alcohol.columns if col != 'Year' and col != 'State']]

new_csv_file_path = "US_alcohol.csv"  
US_alcohol.to_csv(new_csv_file_path, index=False, header=True) 
