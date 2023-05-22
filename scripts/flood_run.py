import configparser
import os
import contextily as cx
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
path_2 = os.path.join(DATA_PROCESSED, 'BGD', 'population.csv')


pop_tif_loc = os.path.join(DATA_RAW, 'WorldPop', 'ppp_2020_1km_Aggregated.tif')
flood_pop = FloodProcess(path, 'BGD', 'inunriver_rcp8p5_0000HadGEM2-ES_2080_rp01000.tif', path_2)
#f = flood_pop.process_flood_tiff()
#shp = flood_pop.process_tif()
#cgdf = flood_pop.pop_flood()
intersection = flood_pop.flood_pop_overlay()