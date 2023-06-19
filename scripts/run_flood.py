import configparser
import os
import pandas as pd
from glanvup.floodzard import FloodProcess
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')

path = os.path.join(DATA_RAW, 'countries.csv')

filename = 'inunriver_rcp8p5_0000HadGEM2-ES_2080_rp01000.tif'
flood_tiff = os.path.join(DATA_RAW, 'flood_hazard', filename)

flooding = FloodProcess(path, 'GBR', flood_tiff)
flood_tiff = flooding.process_flood_tiff()
flood_shp = flooding.process_flood_shapefile()