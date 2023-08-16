import configparser
import os
import warnings
import pandas as pd
from glanvup.preprocess import ProcessCountry, ProcessRegions, ProcessPopulation
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


path = os.path.join(DATA_RAW, 'countries.csv')
pop_tif_loc = os.path.join(DATA_RAW, 'WorldPop', 'ppp_2020_1km_Aggregated.tif')

countries = pd.read_csv(path, encoding = 'latin-1')
income_group = ['LIC', 'LMC', 'UMC']

for idx, country in countries.iterrows():

    #if not country['income_group'] in income_group or country['gid_region'] == 0 or country['Exclude'] == 1:
    if not country['iso3'] == 'BDI':
        
        continue 

    country = ProcessCountry(path, countries['iso3'].loc[idx])
    national_outline = country.process_country_shapes()

    regions = ProcessRegions(countries['iso3'].loc[idx], countries['gid_region'].loc[idx])
    regiona_shapefile = regions.process_regions()

    populations = ProcessPopulation(path, countries['iso3'].loc[idx], countries['gid_region'].loc[idx], pop_tif_loc)
    country_pop = populations.process_national_population()
    region_pop = populations.process_regional_population()
    region_shapefile = populations.pop_process_shapefiles()
    populations.process_country_population()