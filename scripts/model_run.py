import configparser
import os
import numpy as np
import pandas as pd
from glanvup.globpop import GlobalPopulation 
from glanvup.floodzard import FloodProcess
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


path = os.path.join(DATA_RAW, 'countries.csv')


pop_tif_loc = os.path.join(DATA_RAW, 'WorldPop', 'ppp_2020_1km_Aggregated.tif')

## create country folder
#global_population = GlobalPopulation(path, 'GRD', 'GID_0', pop_tif_loc)
#g = global_population.country_directory()

# create a country boundary
#country_line = global_population.country_boundary()

#process country population
#country_pop = global_population.process_population_tif()
#pop_results = pd.DataFrame(country_pop)
#path_out = os.path.join('data', 'processed', 'GRD', 'population.csv')
#pop_results.to_csv(path_out)

flood_pop = FloodProcess(path, 'GRD', 'inunriver_rcp8p5_0000HadGEM2-ES_2080_rp00100.tif')
f = flood_pop.process_flood_tiff()