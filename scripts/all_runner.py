import configparser
import os
import tqdm
import geopandas as gpd
import pandas as pd
from glanvup.floodzard import FloodProcess
from glanvup.preprocess import WealthProcess
from glanvup.coverage import CoverageProcess
from glanvup.intersections import IntersectLayers
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')
DATA_RESULTS = os.path.join(BASE_PATH, 'results')
path = os.path.join(DATA_RAW, 'countries.csv')
flood_folder = os.path.join(DATA_RAW, 'flood_hazard')

flood_files = os.listdir(flood_folder)

countries = pd.read_csv(path, encoding = 'latin-1')
income_group = ['LIC', 'LMC', 'UMC']

for idx, country in countries.iterrows():

    intersected_files = os.path.join(DATA_RESULTS, countries['iso3'].loc[idx], 'pop_hazard_coverage_poverty')

    if not country['iso3'] == 'TUR': 
        continue 

    for file in flood_files:

        try:

            flood_tiff = os.path.join(DATA_RAW, 'flood_hazard', file)

            flooding = FloodProcess(path, countries['iso3'].loc[idx], flood_tiff)
            flooding.process_flood_tiff()
            flooding.process_flood_shapefile()

            wealths = WealthProcess(path, countries['iso3'].loc[idx])
            wealths.process_national_rwi()
            wealths.process_regional_rwi()

            coverages = CoverageProcess(path, countries['iso3'].loc[idx])
            coverages.process_national_coverage()
            coverages.process_regional_coverage()

            intersection = IntersectLayers(countries['iso3'].loc[idx], 'GSM', file)
            intersection.pop_flood()
            intersection.pophaz_coverage()
            intersection.intersect_all()

        except:

            pass