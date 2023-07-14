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

    intersected_files = os.path.join(DATA_RESULTS, 
                                     countries['iso3'].loc[idx], 
                                     'pop_hazard_coverage_poverty')

    if not country['income_group'] in income_group or country['gid_region'] == 0 or country['Exclude'] == 1: 
        continue 

    for file in flood_files:

        try:

            flood_tiff = os.path.join(DATA_RAW, 'flood_hazard', file)

            flooding = FloodProcess(path, countries['iso3'].loc[idx], flood_tiff)
            flooding.process_flood_tiff()
            flooding.process_flood_shapefile()

            wealths = WealthProcess(path, countries['iso3'].loc[idx])
            #wealths.process_national_rwi()
            #wealths.process_regional_rwi()

            coverages = CoverageProcess(path, countries['iso3'].loc[idx])
            #coverages.process_national_coverage()
            #coverages.process_regional_coverage()

            intersection = IntersectLayers(countries['iso3'].loc[idx], '4G', file)
            intersection.pop_flood()
            intersection.pophaz_coverage()
            intersection.intersect_all()

        except:

            pass

coastline = ['IDN', 'PHL', 'MEX', 'BRA', 'TUR', 'IND',
             'PNG', 'ARG', 'MDG', 'MYS', 'CUB', 'VNM', 
             'SOM', 'THA', 'COL', 'VEN', 'ZAF', 'UKR', 
             'EGY', 'IRN', 'PER', 'ECU', 'ERI', 'MMR', 
             'YEM', 'LBY', 'AGO', 'NAM', 'TZA', 'CRI', 
             'DOM', 'TUN', 'PAK', 'JAM', 'LKA', 'DZA',
             'CPV', 'NIC', 'GAB', 'NGA', 'HND', 'MRT', 
             'TLS', 'URY', 'MDV', 'BGD', 'LBR', 'GHA',
             'KEN', 'SEN', 'CIV', 'SEY', 'GUY', 'KHM',
             'CMR', 'SLE', 'GTM', 'BLZ', 'ALB', 'BGR', 
             'GNB', 'GIN', 'DJI', 'GEO', 'SLV', 'GNQ',
             'MNE', 'LBN', 'STP', 'MUS', 'BRN', 'LCA', 
             'DMA', 'BEN', 'GND', 'GMB', 'IRQ', 'TGO', 
             'SVN', 'COD', 'BIH']