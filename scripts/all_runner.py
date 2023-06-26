import configparser
import os
import geopandas as gpd
import pandas as pd
from glanvup.floodzard import FloodProcess
from glanvup.preprocess import WealthProcess
from glanvup.coverage import CoverageProcess
from glanvup.intersections import multi_layers
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')
DATA_RESULTS = os.path.join(BASE_PATH, 'results')
path = os.path.join(DATA_RAW, 'countries.csv')
flood_folder = os.path.join(DATA_RAW, 'flood_hazard')

intersected_files = os.path.join(DATA_RESULTS, 'JAM', 'pop_hazard_coverage_poverty')
flood_files = os.listdir(flood_folder)

for file in flood_files:

    print('Working on {}'.format(file))

    try:
        flood_tiff = os.path.join(DATA_RAW, 'flood_hazard', file)

        flooding = FloodProcess(path, 'JAM', flood_tiff)
        flood_tiff = flooding.process_flood_tiff()
        flood_shp = flooding.process_flood_shapefile()

        wealths = WealthProcess(path, 'JAM')
        country_wealth = wealths.process_national_rwi()
        regional_wealth = wealths.process_regional_rwi() 

        coverages = CoverageProcess(path, 'JAM')
        cov_country = coverages.process_national_coverage()
        cov_region = coverages.process_regional_coverage()

        multi_layers('JAM', 'population', 'river_flood', 'GSM')
        multi_layers('JAM', 'intersection', 'coverage', 'GSM')
        multi_layers('JAM', 'intersection', 'poverty', 'GSM')

        shapefiles = [file for file in os.listdir(intersected_files) if file.endswith('.shp')]

        merged_gdf = gpd.GeoDataFrame()

        for shapefile in shapefiles:
            try:
                print('Generating CSV data for {}'.format(str(shapefile).strip('.shp')))
                shapefile = os.path.join(intersected_files, shapefile)
                gdf = gpd.read_file(shapefile)

                merged_gdf = merged_gdf.append(gdf, ignore_index = True)

                # Select columns to use
                gdf = merged_gdf[['NAME_0', 'NAME_1', 'GID_1', 'value_1', 'value_2', 'geometry']]

                # Calculate the area occupied by vulnerable people
                gdf['area'] = gdf.geometry.area
                gdf = gdf.drop(['geometry'], axis = 1)
                gdf[['scenario', 'period']] = ''

                for i in range(len(gdf)):
                    scenarios = ['historical', 'rcp4p5','rcp8p5']
                    periods = ['rp00100', 'rp01000']
                    for scenario in scenarios:
                        if scenario in file:
                            gdf['scenario'].loc[i] = scenario
            
                    for period in periods:
                        if period in file:
                            gdf['period'].loc[i] = period

                fileout = '{}results.csv'.format(file).replace('.tif', '_')
                folder_out = os.path.join(DATA_RESULTS, 'JAM', 'csv_files')

                if not os.path.exists(folder_out):
                    os.makedirs(folder_out)
                path_out = os.path.join(folder_out, fileout)

                gdf.to_csv(path_out, index = False)

            except:

                pass

    except:

        pass