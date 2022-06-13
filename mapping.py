# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd


dir = '~/downloads/WattTimeTakeHome-main/'


platts = pd.read_csv(dir + 'platts.csv')

entso = pd.read_csv(dir + 'entso.csv')

gppd = pd.read_csv(dir + 'gppd.csv')

#since the platts_plant_id in gppd is not always accurate as per instructions, match first based on plant name

platts_ext_on_name = pd.merge(platts, gppd, left_on = ['plant_name', 'unit_fuel'],right_on = ['plant_name','plant_primary_fuel'])

#do the rest with the platts plant id in gppd
gppd_remaining = gppd[~gppd['platts_plant_id'].isin(platts_ext_on_name['platts_plant_id_y'])]
platts_ext_on_id = pd.merge(platts, gppd_remaining, left_on = [platts['platts_plant_id'].astype(str), platts['unit_fuel']],right_on = [gppd_remaining['platts_plant_id'], gppd_remaining['plant_primary_fuel']]) 

platts_ext_on_name = platts_ext_on_name.drop(columns = ['platts_plant_id_y','owner_x','owner_y','country_x','country_y'])
platts_ext_on_name = platts_ext_on_name.rename(columns = {'platts_plant_id_x':'platts_plant_id'})

platts_ext_on_id = platts_ext_on_id.drop(columns = ['plant_name_y', 'country_x','country_y','owner_x','owner_y','key_0', 'key_1', 'platts_plant_id_y'])
platts_ext_on_id = platts_ext_on_id.rename(columns = {'platts_plant_id_x':'platts_plant_id', 'plant_name_x': 'plant_name'})
platts_total = pd.concat([platts_ext_on_id,platts_ext_on_name])

total = entso.merge(platts_total[['platts_unit_id','gppd_plant_id']],right_on = [platts_total['plant_name'].str.lower(), platts_total['unit_fuel']],left_on = [entso['plant_name'].str.lower(), entso['unit_fuel']])

total[['platts_unit_id','gppd_plant_id','entso_unit_id']].to_csv(dir + 'mapping.csv')
