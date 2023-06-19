import configparser
import os
import warnings
import geopandas as gpd
import pandas as pd
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')
DATA_RESULTS = os.path.join(BASE_PATH, 'results')

path = os.path.join(DATA_RAW, 'countries.csv')

# Population and floods layer
population_folder = os.path.join(BASE_PATH, 'processed', 'KEN', 'population', 'shapefiles')
flood_folder = os.path.join(BASE_PATH, 'processed', 'KEN', 'hazards', 'inunriver', 'shapefiles')

# Output folder
folder_out = os.path.join(DATA_RESULTS, 'KEN', 'pop_hazard')

def intersect_layers(folder_1, folder_2):

    for firstfiles in os.listdir(folder_1):
        
        try:

            if firstfiles.endswith('.shp'):

                first_shapefile = os.path.join(folder_1, firstfiles)
                first_gdf = gpd.read_file(first_shapefile)

                for secondfiles in os.listdir(folder_2):

                    if secondfiles.endswith('.shp'):

                        second_shapefile = os.path.join(folder_2, secondfiles)
                        second_gdf = gpd.read_file(second_shapefile)

                        if firstfiles == secondfiles:

                            print('Intersecting layers for {}'.format(str(firstfiles).strip('.shp')))
                            intersection = gpd.overlay(first_gdf, second_gdf, how = 'intersection')
                            print(intersection)
                            
                            fileout = str(firstfiles)
                            if not os.path.exists(folder_out):
                                os.makedirs(folder_out)
                            path_out = os.path.join(folder_out, fileout)

                            intersection.to_file(path_out, driver = 'ESRI Shapefile')
                            
                        else:

                            print('No Matching shapefile found. Skipping...')
        except:

            pass

    return 'Intersections Completed'

# Population and wealth layer
intersection_1_folder = os.path.join(DATA_RESULTS, 'KEN', 'pop_hazard')
rwi_folder = os.path.join(DATA_PROCESSED, 'KEN', 'coverage', 'regions', 'GSM')

# Output folder
folder_out = os.path.join(DATA_RESULTS, 'KEN', 'pop_haz_cov')

intersect_layers(rwi_folder, intersection_1_folder)