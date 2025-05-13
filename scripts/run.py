import configparser
import os
import warnings
import threading
import pandas as pd
from glanvup.preprocessing import (ProcessCountry, ProcessRegions, ProcessPopulation, PovertyProcess, csv_merger,
combine_region_boundaries)
from glanvup.coverage import CoverageProcess
from concurrent.futures import ProcessPoolExecutor
semaphore = threading.Semaphore()
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


path = os.path.join(DATA_RAW, 'countries.csv')
pop_tif_loc = os.path.join(DATA_RAW, 'WorldPop', 'ppp_2020_1km_Aggregated.tif')
poverty_shp = os.path.join(DATA_RAW, 'poverty_data', 'GSAP2.shp')

countries = pd.read_csv(path, encoding = 'utf-8-sig')
income_group = ['LIC', 'LMC', 'UMC', 'HIC']


for idx, country in countries.iterrows():

    #if not country['income_group'] in income_group or country['lowest'] == 0 or country['Exclude'] == 1:
    if not country['iso3'] == 'GRL': # ESH
        
        continue 

    '''country = ProcessCountry(path, countries['iso3'].loc[idx])
    country.process_country_shapes()

    regions = ProcessRegions(countries['iso3'].loc[idx], countries['lowest'].loc[idx])
    regions.process_regions()
    regions.process_sub_region_boundaries()
    

    populations = ProcessPopulation(path, countries['iso3'].loc[idx], countries['lowest'].loc[idx], pop_tif_loc)
    populations.process_national_population()
    populations.process_population_tif()
    populations.process_sub_regional_pop_tiff()
    populations.pop_process_shapefiles()

    poverty = PovertyProcess(path, countries['iso3'].loc[idx], countries['gid_region'].loc[idx], poverty_shp)
    poverty.country_poverty()

    coverages = CoverageProcess(path, countries['iso3'].loc[idx])
    coverages.process_national_coverage()
    coverages.process_regional_coverage()
    coverages.uncovered_regions()'''

if __name__ == '__main__':

    csv_merger()
    combine_region_boundaries()