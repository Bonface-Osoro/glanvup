import configparser
import os
import re
import shutil
import contextily as cx
import geopandas as gpd
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from glanvup.floodzard import FloodProcess
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')

path = os.path.join(DATA_RAW, 'countries.csv')

filename = 'inunriver_rcp8p5_0000HadGEM2-ES_2080_rp01000.tif'
flood_tiff = os.path.join(DATA_RAW, 'flood_hazard', filename)

#flooding = FloodProcess(path, 'KEN', flood_tiff)
#flood_tiff = flooding.process_flood_tiff()
#flood_shp = flooding.process_flood_shapefile()

folder = os.path.join(DATA_RAW, 'wealth')
pattern = r'_relative_wealth_index'

folder_out = os.path.join(DATA_RAW, 'rwi')

for filename in os.listdir(folder):
    source_file_path = os.path.join(folder, filename)

    if os.path.isfile(source_file_path):
        destination_file_path = os.path.join(folder_out, filename)
    
    shutil.copy2(source_file_path, destination_file_path)

for files in os.listdir(folder_out):

    file_path = os.path.join(folder_out, files)

    if os.path.isfile(file_path):

        new_filename = re.sub(pattern, '', files)

        print(new_filename)

        new_file_path = os.path.join(folder_out, new_filename)

        os.rename(file_path, new_file_path)