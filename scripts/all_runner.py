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

isos = ['ECU', 'EGY', 'ETH', 'FJI', 'GEO', 'GHA', 'GIN', 'GMB', 'GNB', 
        'GTM', 'HND', 'HTI', 'IDN', 'IRM', 'IRQ', 'JOR', 'KAZ', 'KEN', 
        'KGZ', 'KHM', 'LAO', 'LBN', 'LBR', 'LKA', 'LSO', 'MDA', 'MDG', 
        'MEX', 'MLI', 'MMR', 'MOZ', 'MRT', 'MYS', 'NAM', 'NER', 'NGA', 
        'NIC', 'NPL', 'PAK', 'PER', 'PHL', 'PNG', 'RWA', 'SDN', 'SEN', 
        'SLE', 'SLV', 'SOM', 'SRB', 'SYR', 'TCD', 'TGO', 'THA', 'TJK', 
        'TKM', 'TLS', 'TUN', 'TUR', 'TZA', 'UGA', 'UKR', 'UZB', 'VEN', 
        'VNM', 'YEM', 'ZAF', 'ZMB', 'ZWE']

'''for idx, country in countries.iterrows():

    intersected_files = os.path.join(DATA_RESULTS, 
                                     countries['iso3'].loc[idx], 
                                     'pop_hazard_coverage_poverty')

    if not country['income_group'] in income_group or country['gid_region'] == 0 or country['Exclude'] == 1: 
        continue '''
for iso in isos:
    for file in flood_files:

        try:

            flood_tiff = os.path.join(DATA_RAW, 'flood_hazard', file)

            flooding = FloodProcess(path, iso, flood_tiff)
            flooding.process_flood_tiff()
            flooding.process_flood_shapefile()

            wealths = WealthProcess(path, iso)
            #wealths.process_national_rwi()
            #wealths.process_regional_rwi()

            coverages = CoverageProcess(path, iso)
            #coverages.process_national_coverage()
            #coverages.process_regional_coverage()

            intersection = IntersectLayers(iso, '3G', file)
            intersection.pop_flood()
            intersection.pophaz_coverage()
            intersection.intersect_all()

        except:

            pass