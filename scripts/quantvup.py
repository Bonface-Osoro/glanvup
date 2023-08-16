import os
import time
import pandas as pd
import geopandas as gpd
import configparser
from glanvup.rizard import FloodProcess
from glanvup.intersections import IntersectLayers
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))

BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_RESULTS = os.path.join(BASE_PATH, 'processed')

def generate_unconnected_csv(intersect_folder, iso3):
    """
    This function generate a single 
    csv file of unconnected population 
    for an individual country  
    by cellphone technology.
    
    Parameters
    ----------
    intersect_folder : string
        Path of the folder containing 
        intersected shapefiles
    iso3 : string
        Country ISO3 code
    """
    
    print('processing unconnected cellphone {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)

            shapefile[['region', 'income', 'technology']] = ''
            technologies = ['GSM', '3G', '4G']

            for i in range(len(shapefile)):
                
                for technology in technologies:
                    
                    if technology in file_name:

                        shapefile['technology'].loc[i] = technology
            
            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area
            
            shapefile = shapefile[['NAME_0', 'NAME_1', 'value', 
                                   'technology', 'region', 'income']]     

            merged_shapefile = pd.concat([merged_shapefile, 
                                          shapefile], ignore_index = True)       
    
    fileout = '{}_unconnected_results.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def riv_vulnerable_csv(intersect_folder, iso3):
    """
    This function generate a single csv file of 
    vulnerable population to riverine flooding 
    for an individual country by climatic scenario 
    and period.
    
    Parameters
    ----------
    intersect_folder : string
        Path of the folder containing 
        intersected shapefiles
    iso3 : string
        Country ISO3 code
    """
    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    print('processing vulnerable population to riverine flooding {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)
            
            shapefile[['country', 'scenario', 'period', 'continent', 'region', 'income']] = ''
            scenarios = ['historical', 'rcp4p5', 'rcp8p5']
            periods = ['rp00100', 'rp01000']

            for i in range(len(shapefile)):

                shapefile['country'].loc[i] = iso3
                for scenario in scenarios:

                    if scenario in file_name:

                        shapefile['scenario'].loc[i] = scenario

                for period in periods:

                    if period in file_name:

                        shapefile['period'].loc[i] = period
            
            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area
            shapefile = shapefile[['country', 'value_1', 'value_2', 'period', 'scenario', 'area',
                                   'continent', 'region', 'income']]
            merged_shapefile = pd.concat([merged_shapefile, shapefile], ignore_index = True)           

    fileout = '{}_vulnerable_riverine.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def generate_poverty_csv(intersect_folder, iso3):
    """
    This function generate a single 
    csv file of the people living 
    below the poverty level 
    for an individual country  
    by cellphone technology.
    
    Parameters
    ----------
    intersect_folder : string
        Path of the folder containing 
        intersected shapefiles
    iso3 : string
        Country ISO3 code
    """
    
    print('Generating poverty in-line population {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)

            shapefile[['country', 'region', 'income',]] = ''

            for i in range(len(shapefile)):

                shapefile['country'].loc[i] = iso3
                shapefile['value'] = shapefile['value'].round(2)
            
            shapefile = shapefile[['country', 'value', 'rwi', 'region', 'income']]     

            merged_shapefile = pd.concat([merged_shapefile, shapefile], ignore_index = True)       
    
    fileout = '{}_poverty_inline_results.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'povert_inline_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def coast_vulnerable_csv(intersect_folder, iso3):
    """
    This function generate a single csv file of 
    vulnerable population to coastal flooding 
    for an individual country by climatic scenario 
    and period.
    
    Parameters
    ----------
    intersect_folder : string
        Path of the folder containing 
        intersected shapefiles
    iso3 : string
        Country ISO3 code
    """
    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    print('processing vulnerable population to coastalflooding {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)
            
            shapefile[['country', 'scenario', 'period', 'continent', 
                       'region', 'income']] = ''
            scenarios = ['historical', 'rcp4p5', 'rcp8p5']
            periods = ['rp0100', 'rp1000']

            for i in range(len(shapefile)):

                shapefile['country'].loc[i] = iso3
                for scenario in scenarios:

                    if scenario in file_name:

                        shapefile['scenario'].loc[i] = scenario

                for period in periods:

                    if period in file_name:

                        shapefile['period'].loc[i] = period
            
            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area

            shapefile = shapefile[['country', 'value_1', 'value_2', 'period', 'scenario', 'area',
                                   'continent', 'region', 'income']]

            merged_shapefile = pd.concat([merged_shapefile, 
                                          shapefile], 
                                          ignore_index = True)           

    fileout = '{}_vulnerable_coastal.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def generate_vulnerable_averages(iso3, hazard):
    """
    This function calculates the average number of people 
    vulnerable to flooding, the area they occupy and the
    inundation depth of the floods. 
    It also regenerates the aggregate results in the previous function
    by cellphone technology.

    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    """

    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    path_in = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files', 
        '{}_vulnerable_{}.csv'.format(iso3, hazard))
    
    df = pd.read_csv(path_in)
    
    print('Calculating {} average for {}'.format(hazard, iso3))

    flood = df.groupby(['country', 'scenario', 'period'])['value_2'].mean()
    
    population = df.groupby(['country', 'scenario', 'period'])['value_1'].mean()
    
    areas = df.groupby(['country', 'scenario', 'period'])['area'].mean()

    fileout = '{}_{}_depth_average.csv'.format(iso3, hazard)
    fileout_2 = '{}_{}_population_average.csv'.format(iso3, hazard)
    fileout_3 = '{}_{}_area_average.csv'.format(iso3, hazard)
    fileout_4 = '{}_{}_aggregated_results.csv'.format(iso3, hazard)

    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)
    path_out_2 = os.path.join(folder_out, fileout_2)
    path_out_3 = os.path.join(folder_out, fileout_3)
    path_out_4 = os.path.join(folder_out, fileout_4)

    flood.to_csv(path_out)
    population.to_csv(path_out_2)
    areas.to_csv(path_out_3)
    df.to_csv(path_out_4)
    
    return print('Averaging completed for {}'.format(iso3))


def generate_cell_averages(iso3):
    """
    This function calculates the total number of unconected 
    people by cellphone technology for each country.

    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    """

    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    path_in = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files', 
        '{}_unconnected_results.csv'.format(iso3))
    
    df = pd.read_csv(path_in)
    df = df.drop(['NAME_0', 'NAME_1'], axis = 1)

    print('Calculating cellphone average for {}'.format(iso3))
    cellphone = df.groupby(['technology'])['value'].sum()

    fileout = '{}_cellphone_average.csv'.format(iso3)
    folder_out = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    cellphone.to_csv(path_out)
    
    return print('Averaging completed for {}'.format(iso3))


countries = os.listdir(DATA_RESULTS)

######### UNCONNECTED POPULATION #########
'''file = []
technologies = ['GSM', '3G', '4G']

for country in countries:

    try:
        for technology in technologies:

            intersection = IntersectLayers(country, technology, file)
            intersection.pop_coverage()

    except:

        pass'''

######### POOR POPULATION #########
'''file = []
for country in countries:

    try:

        intersection = IntersectLayers(country, 'GSM', file)
        intersection.pop_poverty()

    except:

        pass

DATA_RESULTS = os.path.join(BASE_PATH, 'results')
folders = os.path.join(DATA_RESULTS)
isos = os.listdir(folders)

for iso in isos:

    try:

        folder = os.path.join(folders, iso, 'poor_population')
        generate_poverty_csv(folder, iso)

    except:

        pass'''

######### COASTAL HAZARD VULNERABLE POPULATION #########
'''coastal_folder = os.path.join(DATA_RAW, 'coastal_hazard')
coast_files = os.listdir(coastal_folder)

for country in countries:

    try:
        for file in coast_files:

            if not file.endswith('.DS_Store'):

                intersection = IntersectLayers(country, 'GSM', file)
                intersection.coast_hazard()

    except:

        pass'''

#### PROCESS UNCONNECTED POPULATION CSV FILES ####
if __name__ == '__main__':

    start = time.time()

    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    folders = os.path.join(DATA_RESULTS)
    isos = os.listdir(folders)

    for iso in isos:

        try:

            #folder = os.path.join(folders, iso, 'pop_unconnected')
            #generate_unconnected_csv(folder, iso)

            #folder = os.path.join(folders, iso, 'vul_river_hazard')
            #riv_vulnerable_csv(folder, iso)

            generate_cell_averages(iso)
            #generate_vulnerable_averages(iso, 'riverine')

            #folder = os.path.join(folders, iso, 'vul_coast_hazard')
            #coast_vulnerable_csv(folder, iso)

        except:

            pass

    executionTime = (time.time() - start)