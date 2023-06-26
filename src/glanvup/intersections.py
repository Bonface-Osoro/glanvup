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

def intersect_layers(folder_1, folder_2, folder_out):
    
    """
    This function intersect two shapefiles with 
    similar names located in two different folders 
    and saves the result to a new folder.

    Parameters
    ----------
    folder_1 : string
        Folder path of the first shapefile
    folder_2 : string
        Folder path of the second shapefile
    folder_out : string
        Path of the output folder to store 
        the intersected shapefiles

    """
    for firstfile in os.listdir(folder_1):
        
        try:

            if firstfile.endswith('.shp'):

                first_shapefile = os.path.join(folder_1, firstfile)
                first_gdf = gpd.read_file(first_shapefile)

                for secondfile in os.listdir(folder_2):

                    if secondfile.endswith('.shp'):

                        second_shapefile = os.path.join(folder_2, secondfile)
                        second_gdf = gpd.read_file(second_shapefile)

                        if firstfile == secondfile:

                            print('Intersecting layers for {}'.format(str(firstfile).strip('.shp')))
                            intersection = gpd.overlay(first_gdf, second_gdf, how = 'intersection')
                            
                            fileout = str(firstfile)
                            if not os.path.exists(folder_out):
                                os.makedirs(folder_out)
                            path_out = os.path.join(folder_out, fileout)

                            intersection.to_file(path_out, driver = 'ESRI Shapefile')
                            
                        else:

                            print('No Matching shapefile found. Skipping...')
        except:

            pass

    return None

def multi_layers(iso3, layer_1, layer_2, cell_generation):
    """
    This function uses the intersection function 
    to process multiple layers (population, 
    flood hazard, cellphone coverage and poverty).

    Parameters
    ----------
    iso3 : string
        ISO3 code of the country to process 
        e.g KEN for Kenya.
    layer_1 : string
        Layer type to process. It can ONLY 
        be 'population' or 'intersection'.
    layer_2 : string 
        Second layer to process. It can ONLY 
        be 'river_flood', 'coverage' and 'poverty'.
    cell_generation : string
        Cellphone technology. It can only be 
        'GSM', '3G' or '4G'.

    Returns
    -------
    intersection : geodataframe
        Intersected geodataframe that is 
        saved into a shapefile for visualization.

    """

    #Input folders
    population_folder = os.path.join(DATA_PROCESSED, iso3, 'population', 'shapefiles')
    flood_folder = os.path.join(DATA_PROCESSED, iso3, 'hazards', 'inunriver', 'shapefiles')
    coverage_folder = os.path.join(DATA_PROCESSED, iso3, 'coverage', 'regions', cell_generation)
    rwi_folder = os.path.join(DATA_PROCESSED, iso3, 'rwi', 'regions')

    #Intermediate folders
    intersection_1_folder = os.path.join(DATA_RESULTS, iso3, 'pop_hazard')
    intersection_2_folder = os.path.join(DATA_RESULTS, iso3, 'pop_hazard_coverage')

    #Output folders
    folder_out_1 = os.path.join(DATA_RESULTS, iso3, 'pop_hazard')
    folder_out_2 = os.path.join(DATA_RESULTS, iso3, 'pop_hazard_coverage')
    folder_out_3 = os.path.join(DATA_RESULTS, iso3, 'pop_hazard_coverage_poverty')

    if layer_1 == 'population' and layer_2 == 'river_flood':

        folder_1 = population_folder
        folder_2 = flood_folder
        folder_out = folder_out_1

        intersection = intersect_layers(folder_1, folder_2, folder_out)
    
    elif layer_1 == 'intersection' and layer_2 == 'coverage':

        folder_1 = intersection_1_folder
        folder_2 = coverage_folder
        folder_out = folder_out_2

        intersection = intersect_layers(folder_1, folder_2, folder_out)

    elif layer_1 == 'intersection' and layer_2 == 'poverty':

        folder_1 = intersection_2_folder
        folder_2 = rwi_folder
        folder_out = folder_out_3   

        intersection = intersect_layers(folder_1, folder_2, folder_out)

    else:

        print('Layer not found')

    return None

if __name__ == '__main__':

    multi_layers('KEN', 'population', 'river_flood', 'GSM')
    multi_layers('KEN', 'intersection', 'coverage', 'GSM')
    multi_layers('KEN', 'intersection', 'poverty', 'GSM')