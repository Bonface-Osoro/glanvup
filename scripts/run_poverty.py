import configparser
import os
import warnings
import geopandas as gpd
import pandas as pd
import contextily as ctx
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
from glanvup.preprocess import WealthProcess
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')

path = os.path.join(DATA_RAW, 'countries.csv')

wealths = WealthProcess(path, 'KEN')
country_wealth = wealths.process_national_rwi()
regional_wealth = wealths.process_regional_rwi() 