import configparser
import os 
import shutil
import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot
from glanvup.continents import asia, south_America, north_america, africa, europe 
import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RESULTS = os.path.join(BASE_PATH, 'results')
DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')


def copy_shapefiles(iso3, name_pattern, continent):
    '''
    This function copies the shapefiles of specific 
    hazard period, climatic scenario and cellular 
    technology to a single folder for plotting

    Parameters
    ----------
    iso3 : string
        Specific country ISO3 code
    name_pattern : string
        Name of the shapefile conatining the 
        information about the hazard type, 
        period, climatic scenario and cellular 
        technology type
    continent : string
        Continent where the country belongs to.
    '''

    root_folder = os.path.join(DATA_RESULTS, iso3, 'pop_hazard_coverage_poverty')
    output_folder = os.path.join(BASE_PATH, 'global_results', 'shapefiles', continent) 

    if not os.path.exists(output_folder):

        os.makedirs(output_folder)

    for folder_path, _, files in os.walk(root_folder):

        for file in files:

            if (file.startswith(name_pattern) and file.endswith('.shp') 
                or file.startswith(name_pattern) and file.endswith('.cpg') 
                or file.startswith(name_pattern) and file.endswith('.dbf')
                or file.startswith(name_pattern) and file.endswith('.prj')
                or file.startswith(name_pattern) and file.endswith('.shx')):

                shapefile_path = os.path.join(folder_path, file)
                shutil.copy(shapefile_path, output_folder)
                

def collect_shapefiles(continent):
    '''
    This function collect specific shapefiles 
    based on the hazard type, period, climatic 
    scenario and cellular technology type.

    Parameters
    ----------
    root_folder : string
        Folder path containing the required 
        country shapefiles
    name_pattern : string
        Name of the shapefile conatining the 
        information about the hazard type, 
        period, climatic scenario and cellular 
        technology type
    
    Returns
    -------
    shapefiles : shapefile
        Required shapefiles for plotting.
    '''
    shapefiles = []
    root_folder = os.path.join(BASE_PATH, 'global_results', 'shapefiles', continent)
    country_iso = root_folder.split('/')[2]

    for folder_path, _, files in os.walk(root_folder):

        for file in files:

            print('Collecting {} shapefiles'.format(country_iso))
            if file.endswith('.shp'):

                shapefile_path = os.path.join(folder_path, file)
                gdf = gpd.read_file(shapefile_path)
                shapefiles.append(gdf)

    return shapefiles


def combine_geodataframes(gdfs):
    '''
    This function combines several continental 
    shapefiles into a single one for plotting.

    Parameters
    ----------
    gdf : geodataframe
        Individual geodataframes
    '''
    combined_gdf = gpd.GeoDataFrame(
        pd.concat(gdfs, ignore_index = True), 
        crs = gdfs[0].crs)

    return combined_gdf


def plot_map(gdf, continent):
    '''
    This function plot the shapefiles into 
    a global map

    Parameters
    ----------
    gdf : Geodataframe
        Geodatframe
    continent : string
        Continent of the individual countries
    '''
    sns.set(font_scale = 0.9)
    fig, ax = plt.subplots(figsize = (10, 8))

    bins = [-1e6, 20, 50, 100, 250, 500, 1000, 1500]
    labels = ['<20','20-50','50-100','100-250', '250-500', 
            '500-1k', '1-1.5k']

    gdf = gdf.to_crs(epsg = 4326)

    gdf['bin'] = pd.cut(gdf['value_1'], bins = bins, 
                        labels = labels)
   
    gdf.plot(ax = ax, cmap = 'hsv', #column = 'bin', 
                linewidth = 0, legend = True, antialiased = False)

    cx.add_basemap(ax, crs = 'epsg:4326', source = cx.providers.Stamen.Terrain)
    name = 'Distribution of Poor, Unconnected to 3G and \nVulnerable Population to Riverine Flooding in {}'.format(continent)
    name = ''
    fig.suptitle(name)
    plt.suptitle(name, fontsize = 13, wrap = True)

    path = os.path.join(DATA_VIS, '{}_global_map.png'.format(continent))
    plt.savefig(path)
    #plt.show()

if __name__ == '__main__':

    folders = os.path.join(DATA_RESULTS)
    
    isos = ['UKR']
    
    name_pattern = 'nunriver_historical_000000000WATCH_1980_rp00100_'
    for iso in isos:
        print('skip')
        copy_shapefiles(iso, name_pattern, 'UKR')

    global_shapefiles = collect_shapefiles('UKR')
    combined_gdf = combine_geodataframes(global_shapefiles)
    plot_map(combined_gdf, 'UKR')