import pandas as pd
import csv


raw_forest_data = pd.read_csv('annual-change-forest-area.csv', sep=',')
raw_co2_data = pd.read_csv('co2_emission.csv', sep=',')
raw_temp_change_data = pd.read_csv('Environment_Temperature_change_E_All_Data_NOFLAG.csv', sep=',', encoding_errors='ignore')
temp_data = pd.read_csv('GlobalLandTemperaturesByCountry.csv', sep=',')
red_index_data = pd.read_csv('red_list_index_country_timeseries.csv', sep=',')
red_index_data = red_index_data[red_index_data['VAR'] == 'INDEX']

temp_change_data = raw_temp_change_data.melt(id_vars=['Area Code', 'Area', 'Months Code',
    'Months', 'Element Code', 'Element', 'Unit'
    ],
    var_name='Year',
    value_name="Temperature Change"
)

forest_data = raw_forest_data.rename({'Entity': 'Country'}, axis=1)
co2_data = raw_co2_data.rename({'Entity': 'Country'}, axis=1)
temp_change_data = temp_change_data.rename({'Area': 'Country'}, axis=1)

temp_change_data = temp_change_data[temp_change_data['Months'] == 'Meteorological year']
temp_change_data['Year'] = temp_change_data['Year'].str.replace('Y', '')


temp_data['Year'] = pd.to_numeric(temp_data['dt'].str[:4])
forest_data['Country'] = forest_data['Country'].astype('|S').str.decode(encoding='UTF-8')
co2_data['Country'] = co2_data['Country'].astype('|S').str.decode(encoding='UTF-8')
temp_change_data['Country'] = temp_change_data['Country'].astype('|S').str.decode(encoding='UTF-8')
temp_change_data['Year'] = pd.to_numeric(temp_change_data['Year'])

with open('paises_diferentes.csv', newline='') as csvfile:
    CSVreader = csv.reader(csvfile, delimiter=',')
    for row in CSVreader:
        dataframe = row[0]
        original = row[1]
        unified = row[2]
        if dataframe == 'CO2':
            co2_data[co2_data['Country'] == original]['Country'] = unified
        elif dataframe == 'forest':
            forest_data[forest_data['Country'] == original]['Country'] = unified
        elif dataframe == 'delta':
            temp_change_data[temp_change_data['Country'] == original]['Country'] = unified
        

dataset = pd.merge(temp_data, co2_data, on=['Year', 'Country'], how='left')
dataset = pd.merge(dataset, forest_data, on=['Year', 'Country'], how='left')
dataset = pd.merge(dataset, temp_change_data, on=['Year', 'Country'], how='left')
dataset = pd.merge(dataset, red_index_data, on=['Year', 'Country'], how='left')

dataset = dataset[dataset['Year'] > 1959]

dataset.to_csv('clean_dataset.csv', index=False)
red_index_data.to_csv('red_index_data.csv', index=False)