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


class IntersectLayers:

    """
    This class intersect all the processed layers.
    """


    def __init__(self, country_iso3, cell_gen, flood_file):
        """
        A class constructor

        Arguments
        ---------
        country_iso3 : string
            Country iso3 to be processed..
        cell_generation : string
            Cellphone technology. It can only be 
            'GSM', '3G' or '4G'.
        flood_file : string
            Name of the flood layer containing 
            the scenario and period information
        """
        self.country_iso3 = country_iso3
        self.cell_gen = cell_gen
        self.flood_file = flood_file


    def intersect_layers(self, folder_1, folder_2, folder_out):

        for firstfile in os.listdir(folder_1):
            
            try:

                if firstfile.endswith('.shp'):

                    first_shapefile = os.path.join(folder_1, firstfile)
                    first_gdf = gpd.read_file(first_shapefile)

                    for secondfile in os.listdir(folder_2):

                        if secondfile.endswith('.shp'):

                            second_shapefile = os.path.join(folder_2, secondfile)
                            second_gdf = gpd.read_file(second_shapefile)

                            if firstfile in secondfile:

                                intersection = gpd.overlay(first_gdf, second_gdf, how = 'intersection')
                                
                                region_part = str(firstfile)
                                
                                if not os.path.exists(folder_out):

                                    os.makedirs(folder_out)

                                path_out = os.path.join(folder_out, region_part)

                                intersection.to_file(path_out, driver = 'ESRI Shapefile')
                                
                            else:

                                print('No Matching shapefile found. Skipping...')
            except:

                pass


        return None
    
    def pop_flood(self):

        population_folder = os.path.join(DATA_PROCESSED, self.country_iso3, 'population', 'shapefiles')
        flood_folder = os.path.join(DATA_PROCESSED, self.country_iso3, 'hazards', 'inunriver', 'shapefiles')
        folder_out_1 = os.path.join(DATA_RESULTS, self.country_iso3, 'pop_hazard')
        if not os.path.exists(folder_out_1):

            os.makedirs(folder_out_1)

        intersection = IntersectLayers.intersect_layers(self, population_folder, flood_folder, folder_out_1)

        return None
    
    def pophaz_coverage(self):

        intersection_1_folder = os.path.join(DATA_RESULTS, self.country_iso3, 'pop_hazard')
        coverage_folder = os.path.join(DATA_PROCESSED, self.country_iso3, 'coverage', 'regions', self.cell_gen)
        folder_out_2 = os.path.join(DATA_RESULTS, self.country_iso3, 'pop_hazard_coverage')
        if not os.path.exists(folder_out_2):

            os.makedirs(folder_out_2)

        intersection = IntersectLayers.intersect_layers(self, intersection_1_folder, coverage_folder, folder_out_2)

        return None
    
    def intersect_all(self):

        intersection_2_folder = os.path.join(DATA_RESULTS, self.country_iso3, 'pop_hazard_coverage')
        rwi_folder = os.path.join(DATA_PROCESSED, self.country_iso3, 'rwi', 'regions')

        for firstfile in os.listdir(intersection_2_folder):
            
            try:

                if firstfile.endswith('.shp'):

                    first_shapefile = os.path.join(intersection_2_folder, firstfile)
                    first_gdf = gpd.read_file(first_shapefile)

                    for secondfile in os.listdir(rwi_folder):

                        if secondfile.endswith('.shp'):

                            second_shapefile = os.path.join(rwi_folder, secondfile)
                            second_gdf = gpd.read_file(second_shapefile)

                            if firstfile in secondfile:

                                intersection = gpd.overlay(first_gdf, second_gdf, how = 'intersection')
                                
                                cell_generation = str(self.cell_gen)
                                region_part = str(firstfile)
                                flood_part = str(self.flood_file).strip('.tif')
                                
                                filename = '{}_{}_{}'.format(cell_generation, flood_part, region_part)

                                folder_out_3 = os.path.join(DATA_RESULTS, self.country_iso3, 'pop_hazard_coverage_poverty')
                                if not os.path.exists(folder_out_3):

                                    os.makedirs(folder_out_3)
                                    
                                path_out = os.path.join(folder_out_3, filename)

                                intersection.to_file(path_out, driver = 'ESRI Shapefile')
                                
                            else:

                                print('Skipping population, poverty and coverage intersection...missing data')
            except:

                pass

        return None


'''if __name__ == '__main__':

    inter = IntersectLayers()
    inter.pop_flood()
    inter.pophaz_coverage()
    inter.intersect_all()'''