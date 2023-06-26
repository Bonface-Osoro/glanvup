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

DATA_RESULTS = os.path.join(BASE_PATH, 'results')
intersected_files = os.path.join(DATA_RESULTS, 'KEN', 'pop_hazard_coverage_poverty')

def quantify(folder_path, iso3):

    """
    This function quantifies the number of 
    people vulnerable to climate-driven 
    natural hazards living below the poverty 
    line and have no cellphone coverage. 
    It also calculates the total area of 
    where they are.

    Parameters
    ----------
    folder_path : string
        Folder path of the shapefile
    iso3 : string
        country Iso3 code eg Kenya is KEN
    """

    shapefiles = [file for file in os.listdir(folder_path) if file.endswith('.shp')]

    merged_gdf = gpd.GeoDataFrame()

    for shapefile in shapefiles:
        try:
            print('Generating CSV data for {}'.format(str(shapefile).strip('.shp')))
            shapefile = os.path.join(folder_path, shapefile)
            gdf = gpd.read_file(shapefile)

            merged_gdf = merged_gdf.append(gdf, ignore_index = True)

            # Select columns to use
            gdf = merged_gdf[['NAME_0', 'NAME_1', 'GID_1', 'value_1', 'value_2', 'geometry']]

            # Calculate the area occupied by vulnerable people
            gdf['area'] = gdf.geometry.area
            gdf = gdf.drop(['geometry'], axis = 1)
            gdf[['scenario', 'period']] = ''

            fileout = 'intersected.csv'
            folder_out = os.path.join(DATA_RESULTS, iso3, 'csv_files')

            if not os.path.exists(folder_out):
                os.makedirs(folder_out)
            path_out = os.path.join(folder_out, fileout)

            gdf.to_csv(path_out, index = False)

        except:

            pass

    return None
    

quantify(intersected_files, 'KEN')