import os
import pandas as pd
import geopandas as gpd
import configparser
import time
import warnings
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RESULTS = os.path.join(BASE_PATH, 'results')

def generate_aggregate_csv(intersect_folder, iso3):
    """
    This function generate a single 
    csv file for an individual country  
    by climate hazard scenario and return 
    period.
    
    Parameters
    ----------
    intersect_folder : string
        Path of the folder containing 
        intersected shapefiles
    iso3 : string
        Country ISO3 code
    """
    
    print('processing coastal flooding {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)

            shapefile[['scenario', 'period', 'technology']] = ''
            scenarios = ['historical', 'rcp4p5', 'rcp8p5']
            periods = ['rp0100', 'rp1000']
            technologies = ['GSM', '3G', '4G']

            for i in range(len(shapefile)):

                for scenario in scenarios:

                    if scenario in file_name:

                        shapefile['scenario'].loc[i] = scenario

                for period in periods:

                    if period in file_name:

                        shapefile['period'].loc[i] = period
                
                for technology in technologies:
                    
                    if technology in file_name:

                        shapefile['technology'].loc[i] = technology

            shapefile = shapefile[['NAME_0', 'NAME_1', 'value_1', 
                                   'value_2', 'period', 'scenario', 
                                   'technology', 'geometry']]

            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area

            merged_shapefile = pd.concat([merged_shapefile, 
                                          shapefile], 
                                          ignore_index = True)           

    fileout = '{}_aggregated_results.csv'.format(iso3, 
                                                 merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'coastal_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def generate_averages(iso3):
    """
    This function calculates the average number of people 
    vulnerable to flooding, the area they occupy and the
    inundation depth of the floods. 
    It also regenerates the aggregate results in the previous function
    by cellphone technology.
    """

    path_in = os.path.join(
        DATA_RESULTS, iso3, 'coastal_csv_files', 
        '{}_aggregated_results.csv'.format(iso3))
    
    df = pd.read_csv(path_in)
    
    print('Calculating coastal flood average for {}'.format(iso3))

    df = df.fillna('GSM')

    flood = df.groupby(['NAME_0', 'scenario', 'technology',
                        'period'])['value_2'].mean()
    
    population = df.groupby(['NAME_0', 'scenario', 'technology',
                             'period'])['value_1'].mean()
    
    areas = df.groupby(['NAME_0', 'scenario', 'technology',
                        'period'])['area'].mean()

    fileout = '{}_flood_average.csv'.format(iso3)
    fileout_2 = '{}_population_average.csv'.format(iso3)
    fileout_3 = '{}_area_average.csv'.format(iso3)
    fileout_4 = '{}_aggregated_results.csv'.format(iso3)

    folder_out = os.path.join(DATA_RESULTS, iso3, 
                              'coastal_csv_files')

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


if __name__ == '__main__':

    start = time.time()

    folders = os.path.join(DATA_RESULTS)
    isos = os.listdir(folders)
    
    for iso in isos:

        try:

            folder = os.path.join(folders, iso, 'pop_cozard_coverage_poverty')
            generate_aggregate_csv(folder, iso)
            generate_averages(iso)

        except:

            pass

    executionTime = (time.time() - start)

    print('Execution time in minutes: ' + str(round(executionTime / 60, 2)))