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
path_2 = os.path.join(DATA_PROCESSED, 'RWA', 'population.csv')


pop_tif_loc = os.path.join(DATA_RAW, 'WorldPop', 'ppp_2020_1km_Aggregated.tif')
filename = 'inunriver_rcp8p5_0000HadGEM2-ES_2080_rp01000.tif'

flood_pop = FloodProcess(path, 'RWA', filename, path_2)
f = flood_pop.process_flood_tiff()
shp = flood_pop.process_tif()
cgdf = flood_pop.pop_flood()
merging = flood_pop.flood_pop_merge()
intersection = flood_pop.intersect_layers()

fig, ax = plt.subplots(1, 1, figsize=(5, 6)) 
fig.set_facecolor('gainsboro')

# Import hazard and plot 
hazard = cgdf
hazard.plot(color = 'blue', linewidth = 1.5, alpha = .7, legend = True, edgecolor = None, ax = ax)

cx.add_basemap(ax, crs = 'epsg:4326', source = cx.providers.Stamen.Terrain) #add the map baselayer

# Subset scenario strings for title
hazard_type = filename.split('_')[0]
scenario = filename.split('_')[1]
model = filename.split('_')[2]
year = filename.split('_')[3]
return_period = filename.split('_')[4]
return_period = return_period.replace('.tif', '')

# Insert scenario strings in title
main_title = 'Projected River Flooding:\n{}, {}, {}, {}, {}, {}'.format(
    'RWA', hazard_type, scenario, model, year, return_period)

plt.suptitle(main_title, fontsize = 13, wrap = True)
path = os.path.join('data', 'processed', 'RWA', main_title)
fig.savefig(path, dpi = 720)
plt.close(fig)

quant = flood_pop.quantification()
