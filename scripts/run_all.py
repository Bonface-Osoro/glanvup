import os
import time
import configparser
import pandas as pd
from glanvup.rizard import FloodProcess
from glanvup.cozard import CoastProcess
from glanvup.intersections import IntersectLayers
from glanvup.continents import south_coast
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')
DATA_RESULTS = os.path.join(BASE_PATH, 'results')

path = os.path.join(DATA_RAW, 'countries.csv')
flood_folder = os.path.join(DATA_RAW, 'flood_hazard')
coastal_folder = os.path.join(DATA_RAW, 'coastal_hazard')

flood_files = os.listdir(flood_folder)
coast_files = os.listdir(coastal_folder)

countries = pd.read_csv(path, encoding = 'utf-8-sig')
income_group = ['LIC', 'LMC', 'UMC']

for idx, country in countries.iterrows():

    if not country['income_group'] in income_group or country['gid_region'] == 0 or country['Exclude'] == 1:
    #if not country['iso3'] == 'RWA':

        continue 
    
    for file in flood_files:

        if not file.startswith('.DS_Store'):

            flood_tiff = os.path.join(DATA_RAW, 'flood_hazard', file)

            flooding = FloodProcess(path, countries['iso3'].loc[idx], flood_tiff)
            flooding.process_flood_tiff()
            flooding.process_flood_shapefile()
            
            intersection = IntersectLayers(countries['iso3'].loc[idx], 'GSM', file)
            intersection.pop_flood()
            intersection.vulri_intersect_all()
            intersection.coverage_rizard()

    '''for file in coast_files:
        
        try:

            coastal_tiff = os.path.join(DATA_RAW, 'coastal_hazard', file)

            coastal = CoastProcess(path, countries['iso3'].loc[idx], coastal_tiff)
            coastal.process_flood_tiff() 
            coastal.process_flood_shapefile()

            intersection = IntersectLayers(countries['iso3'].loc[idx], 'GSM', file)
            intersection.pop_cozard()
            intersection.vulco_intersect_all()
            intersection.coverage_cozard()

        except:

            pass'''