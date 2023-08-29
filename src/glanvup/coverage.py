import configparser
import os 
import rasterio
import warnings
import contextily as cx
import geopandas as gpd   
import matplotlib.pyplot as plt
import pandas as pd       
import seaborn as sns
from rasterio.mask import mask
from shapely.geometry import MultiPolygon
from tqdm import tqdm
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


def clean_coverage(x):
    """
    Cleans the coverage polygons by removing 
    small multipolygon shapes.

    Parameters
    ---------
    x : polygon
        Feature to simplify.

    Returns
    -------
    MultiPolygon : MultiPolygon
        Shapely MultiPolygon geometry without tiny shapes.

    """
    # if its a single polygon, just return the polygon geometry
    if x.geometry.geom_type == 'Polygon':

        if x.geometry.area > 1e7:

            return x.geometry

    # if its a multipolygon, we start trying to simplify and
    # remove shapes if its too big.
    elif x.geometry.geom_type == 'MultiPolygon':

        threshold = 1e7

        # save remaining polygons as new multipolygon for
        # the specific country
        new_geom = []
        for y in x.geometry:

            if y.area > threshold:
                
                new_geom.append(y)

        return MultiPolygon(new_geom)


class CoverageProcess:
    """
    This class process the flood layers using the country boundary.
    """

    def __init__(self, csv_filename, country_iso3):
        """
        A class constructor.

        Arguments
        ---------
        csv_filename : string
            Name of the country metadata file.
        country_iso3 : string
            Country iso3 to be processed.
        """
        self.csv_filename = csv_filename
        self.country_iso3 = country_iso3


    def process_national_coverage(self):

        countries = pd.read_csv(self.csv_filename, encoding = 'latin-1')

        for idx, country in countries.iterrows():
            
            if not country['iso3'] == self.country_iso3: 

                continue  
            iso3 = country['iso3']
            iso2 = country['iso2']

            technologies = ['GSM', '3G', '4G']

            for tech in technologies:

                folder_coverage = os.path.join(DATA_PROCESSED, iso3, 'coverage', 'national')
                filename = 'coverage_{}.shp'.format(tech)
                path_output = os.path.join(folder_coverage, filename)

                if os.path.exists(path_output):

                    continue

                print('Working on {} in {}'.format(tech, iso3))

                filename = 'Inclusions_201812_{}.shp'.format(tech)
                folder = os.path.join(DATA_RAW, 'mobile_coverage_explorer_2019',
                    'Data_MCE')
                inclusions = gpd.read_file(os.path.join(folder, filename))

                if iso2 in inclusions['CNTRY_ISO2']:

                    filename = 'MCE_201812_{}.shp'.format(tech)
                    folder = os.path.join(DATA_RAW, 'mobile_coverage_explorer_2019',
                        'Data_MCE')
                    coverage = gpd.read_file(os.path.join(folder, filename))

                    coverage = coverage.loc[coverage['CNTRY_ISO3'] == iso3]

                else:

                    filename = 'OCI_201812_{}.shp'.format(tech)
                    folder = os.path.join(DATA_RAW, 'mobile_coverage_explorer_2019',
                        'Data_OCI')
                    coverage = gpd.read_file(os.path.join(folder, filename))

                    coverage = coverage.loc[coverage['CNTRY_ISO3'] == iso3]

                if len(coverage) > 0:

                    print('Dissolving polygons')
                    coverage['dissolve'] = 1
                    coverage = coverage.dissolve(by = 'dissolve', aggfunc='sum')

                    coverage = coverage.to_crs({'init': 'epsg:3857'})

                    print('Excluding small shapes')
                    coverage['geometry'] = coverage.apply(clean_coverage, axis = 1)

                    print('Removing empty and null geometries')
                    coverage = coverage[~(coverage['geometry'].is_empty)]
                    coverage = coverage[coverage['geometry'].notnull()]

                    print('Simplifying geometries')
                    coverage['geometry'] = coverage.simplify(tolerance = 0.005,
                        preserve_topology = True).buffer(0.0001).simplify(
                        tolerance = 0.005, preserve_topology = True)

                    coverage = coverage.to_crs({'init': 'epsg:4326'})

                    if not os.path.exists(folder_coverage):

                        os.makedirs(folder_coverage)

                    coverage.to_file(path_output, driver = 'ESRI Shapefile')

            print('Processed coverage shapes')


    def process_regional_coverage(self):
        """
        Function to process coverage of a single region 
        of an LMIC country.  
        """
        countries = pd.read_csv(self.csv_filename, encoding = 'latin-1')

        iso3 = self.country_iso3

        for idx, country in countries.iterrows():

            if not country["iso3"] == iso3:

                continue

            iso3 = country['iso3']                 
            gid_region = country['gid_region']
            #gid_level = 'GID_{}'.format(gid_region)
            large_countries = ['ARG', 'BRA', 'CHN', 'USA', 'DZA', 'IND', 'RUS']
            if country['iso3'] in large_countries:
                
                filename = 'regions_1_{}.shp'.format(iso3)
                gid_level = 'GID_1'

            else:

                filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
                gid_level = 'GID_{}'.format(gid_region)

            folder = os.path.join('data','processed', iso3, 'regions')
            path_regions = os.path.join(folder, filename)

            regions = gpd.read_file(path_regions, crs = 'epsg:4326')

            for idx, region in regions.iterrows():

                gid_id = region[gid_level]

                if country['iso3'] in large_countries:
                    
                    filename = 'regions_1_{}.shp'.format(iso3)
                    gid_level = 'GID_1'

                else:

                    filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
                    gid_level = 'GID_{}'.format(gid_region)
                path_region = os.path.join(DATA_PROCESSED, iso3, 'regions', filename)

                gdf_region = gpd.read_file(path_region, crs = 'EPSG:4326')

                technologies = ['GSM', '3G', '4G']

                for tech in tqdm(technologies, desc = 'Processing coverage shapefiles for {} coverage'.format(iso3)):
                    
                    #loading in coverage info
                    filename = 'coverage_{}.shp'.format(tech) 
                    folder= os.path.join(DATA_PROCESSED, iso3 , 'coverage', 'national')
                    path_cov= os.path.join(folder, filename)

                    gdf_cov = gpd.read_file(path_cov, crs = 'EPSG:4326')
                    gdf_region = gdf_region[gdf_region[gid_level] == gid_id]

                    print('Intersecting {} coverage datapoints'.format(tech))

                    gdf_cov = gpd.overlay(gdf_cov, gdf_region, how = 'intersection')

                    filename = '{}.shp'.format(gid_id)
                    folder_out = os.path.join(BASE_PATH, 'processed', iso3, 'coverage', 'regions', tech)

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, filename)

                    if gdf_cov.empty:

                        continue

                    else:
                        gdf_cov.to_file(path_out, crs = 'EPSG:4326')

        return print('Regional coverage processing completed for {}'.format(iso3))