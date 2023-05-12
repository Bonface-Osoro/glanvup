import configparser
import os
import numpy as np
import pandas as pd
from glanvup.globpop import GlobalPopulation 
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA = os.path.join('data')
RESULTS = os.path.join('results')
VIS = os.path.join('vis')

path = os.path.join(DATA, 'countries.csv')
metadata_file = pd.read_csv(path)
global_population = GlobalPopulation(metadata_file, 'KEN')