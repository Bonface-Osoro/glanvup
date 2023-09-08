import configparser
import json
import os
import rasterio
import geopandas as gpd
import pandas as pd
from rasterio.mask import mask
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from tqdm import tqdm

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')

def remove_small_shapes(x):
    """
    Remove small multipolygon shapes.

    Parameters
    ---------
    x : polygon
        Feature to simplify.

    Returns
    -------
    MultiPolygon : MultiPolygon
        Shapely MultiPolygon geometry without tiny shapes.

    """
    if x.geometry.type == 'Polygon':

        return x.geometry

    elif x.geometry.type == 'MultiPolygon':

        area1 = 0.01
        area2 = 50

        if x.geometry.area < area1:
            return x.geometry

        if x['GID_0'] in ['CHL','IDN']:

            threshold = 0.01

        elif x['GID_0'] in ['RUS','GRL','CAN','USA']:

            threshold = 0.01

        elif x.geometry.area > area2:

            threshold = 0.1

        else:

            threshold = 0.001

        new_geom = []
        for y in list(x['geometry'].geoms):

            if y.area > threshold:

                new_geom.append(y)

        return MultiPolygon(new_geom)


class ProcessCountry:

    """
    This class process the country folders and
    the national outline shapefile.
    """


    def __init__(self, csv_country, country_iso3):
        """
        A class constructor

        Arguments
        ---------
        csv_country : string
            Name of the country metadata file.
        country_iso3 : string
            Country iso3 to be processed.
        """
        self.csv_country = csv_country
        self.country_iso3 = country_iso3


    def get_countries(self):
        """
        Get all countries.

        Returns
        -------
        countries : dataframe
            Dataframe containing all the country metadata.

        """
        countries = pd.read_csv(self.csv_country, encoding = 'latin-1')

        countries = countries[countries.Exclude == 0]
        
        countries = countries.sample(frac = 1)

        return countries
    

    def process_country_shapes(self):
        """
        This function creates regional folders for each country 
        and then process a national outline shapefile.

        """          
        path = os.path.join('data', 'processed', self.country_iso3)

        if os.path.exists(os.path.join(path, 'national_outline.shp')):

            print('Completed national outline processing')
            
        print('Processing country shapes')

        if not os.path.exists(path):

            os.makedirs(path)

        shape_path = os.path.join(path, 'national_outline.shp')

        path = os.path.join('data', 'raw', 'GADM', 'gadm36_0.shp')

        countries = gpd.read_file(path)

        single_country = countries[countries.GID_0 == self.country_iso3].reset_index()

        single_country = single_country.copy()
        single_country['geometry'] = single_country.geometry.simplify(
            tolerance = 0.01, preserve_topology = True)
        
        single_country['geometry'] = single_country.apply(
            remove_small_shapes, axis = 1)
        
        glob_info_path = os.path.join(self.csv_country)
        load_glob_info = pd.read_csv(glob_info_path, encoding = 'ISO-8859-1', 
                                     keep_default_na = False)
        
        single_country = single_country.merge(load_glob_info, left_on = 'GID_0', 
            right_on = 'iso3')
        
        single_country.to_file(shape_path)

        return print('National outline shapefile processing completed for {}'.format(self.country_iso3))


class ProcessRegions:

    """
    This class process the country folders and
    the national outline shapefile.
    """


    def __init__(self, country_iso3, gid_level):
        """
        A class constructor

        Arguments
        ---------
        country_iso3 : string
            Country iso3 to be processed..
        gid_level : integer
            Gid level to process.
        """
        self.gid_level = gid_level
        self.country_iso3 = country_iso3


    def process_regions(self):
        """
        Function for processing the lowest desired subnational
        regions for the chosen country.
        """
        regions = []

        for regional_level in range(1, int(self.gid_level) + 1): 

            filename = 'regions_{}_{}.shp'.format(regional_level, self.country_iso3)
            folder = os.path.join('data', 'processed', self.country_iso3, 'regions')
            path_processed = os.path.join(folder, filename)

            if os.path.exists(path_processed):

                continue

            print('Processing GID_{} region shapes'.format(regional_level))

            if not os.path.exists(folder):

                os.mkdir(folder)

            filename = 'gadm36_{}.shp'.format(regional_level)
            path_regions = os.path.join('data', 'raw', filename)
            regions = gpd.read_file(path_regions)

            regions = regions[regions.GID_0 == self.country_iso3]

            regions = regions.copy()
            regions['geometry'] = regions.geometry.simplify(
                tolerance=0.005, preserve_topology=True)

            regions['geometry'] = regions.apply(remove_small_shapes, axis = 1)

            try:

                regions.to_file(path_processed, driver = 'ESRI Shapefile')

            except:

                print('Unable to write {}'.format(filename))

                pass

        return print('Regional shapefiles processing completed for {}'.format(self.country_iso3))
    
    def process_sub_region_boundaries(self):

        region_path = '../' 
        countries = gpd.read_file(region_path)

        for index, row in tqdm(countries.iterrows(), desc = 'Processing sub-region boundaries'):

            sub_region_shapefile = gpd.GeoDataFrame([row], crs = countries.crs)

            filename = '{}.shp'.format(row['GID_1'])    

            folder_out = os.path.join('data', 'processed', self.country_iso3, 'boundaries')

            if not os.path.exists(folder_out):

                os.makedirs(folder_out)

            path_out = os.path.join(folder_out, filename)

            sub_region_shapefile.to_file(path_out, driver = 'ESRI Shapefile')

        return print('Sub-region boundary processed')


class ProcessPopulation:
    """
    This class process the country folders and
    the national outline shapefile.
    """


    def __init__(self, csv_country, country_iso3, gid_region, pop_tiff):
        """
        A class constructor

        Arguments
        ---------
        csv_country : string
            Name of the country metadata file.
        country_iso3 : string
            Country iso3 to be processed.
        gid_region: string
            GID boundary spatial level to process
        pop_tiff: string
            Filename of the population raster layer

        """
        self.csv_country = csv_country
        self.country_iso3 = country_iso3
        self.pop_tiff = pop_tiff
        self.gid_region = gid_region


    def process_national_population(self):

        """
        This function creates a national population .tiff
        using national boundary files created in 
        process_national_boundary function
        """

        iso3 = self.country_iso3
        gid_region = self.gid_region

        filename = self.pop_tiff
        path_pop = os.path.join(filename)
        hazard = rasterio.open(path_pop, 'r+')
        hazard.nodata = 255                       
        hazard.crs.from_epsg(4326) 

        filename = 'national_outline.shp'
        folder = os.path.join('data', 'processed', self.country_iso3)
        
        #then load in our country as a geodataframe
        path_in = os.path.join(folder, filename)
        country_pop = gpd.read_file(path_in, crs = 'epsg:4326')

        #create a new gpd dataframe from our single country geometry
        geo = gpd.GeoDataFrame(gpd.GeoSeries(country_pop.geometry))

        #this line sets geometry for resulting geodataframe
        geo = geo.rename(columns={0:'geometry'}).set_geometry('geometry')

        #convert to json
        coords = [json.loads(geo.to_json())['features'][0]['geometry']]        

        #carry out the clip using our mask
        out_img, out_transform = mask(hazard, coords, crop = True)

        #update our metadata
        out_meta = hazard.meta.copy()
        out_meta.update({'driver': 'GTiff', 'height': out_img.shape[1],
                        'width': out_img.shape[2], 'transform': out_transform,
                        'crs': 'epsg:4326'})
        
        #now we write out at the regional level
        filename_out = 'ppp_2020_1km_Aggregated.tif' #each regional file is named using the gid id
        folder_out = os.path.join('data', 'processed', iso3, 'population', 'national')

        if not os.path.exists(folder_out):

            os.makedirs(folder_out)

        path_out = os.path.join(folder_out, filename_out)

        with rasterio.open(path_out, 'w', ** out_meta) as dest:

            dest.write(out_img)

        return print('Population processing completed for {}'.format(iso3))
    
    def process_country_population(self):
        """
        This function process each of the population 
        raster layers to vector shapefiles
        """
        folder = os.path.join('data', 'processed', self.country_iso3, 'population', 'national')

        for tifs in tqdm(os.listdir(folder), 
                         desc = 'Processing {} population shapefile'.format(self.country_iso3)):
            try:

                if tifs.endswith('.tif'):

                    tifs = os.path.splitext(tifs)[0]

                    folder = os.path.join('data', 'processed', self.country_iso3, 'population', 'national')
                    filename = tifs + '.tif'
                    
                    path_in = os.path.join(folder, filename)

                    folder = os.path.join('data', 'processed', self.country_iso3, 'population', 'country_shapefile')
                    if not os.path.exists(folder):

                        os.mkdir(folder)
                        
                    filename = self.country_iso3 + '.shp'
                    path_out = os.path.join(folder, filename)

                    with rasterio.open(path_in) as src:

                        affine = src.transform
                        array = src.read(1)

                        output = []

                        for vec in rasterio.features.shapes(array):

                            if vec[1] > 0 and not vec[1] == 255:

                                coordinates = [i for i in vec[0]['coordinates'][0]]

                                coords = []

                                for i in coordinates:

                                    x = i[0]
                                    y = i[1]

                                    x2, y2 = src.transform * (x, y)

                                    coords.append((x2, y2))

                                output.append({
                                    'type': vec[0]['type'],
                                    'geometry': {
                                        'type': 'Polygon',
                                        'coordinates': [coords],
                                    },
                                    'properties': {
                                        'value': vec[1],
                                    }
                                })

                    output = gpd.GeoDataFrame.from_features(output, crs = 'epsg:4326')
                    output.to_file(path_out, driver = 'ESRI Shapefile')

            except:

                pass

        return None


    def process_regional_population(self):
        """
        This function creates a regional composite population .tiff 
        using regional boundary files created in 
        process_regional_boundary function and national
        population files created in process_national_population
        function.
        """
        countries = pd.read_csv(self.csv_country, encoding = 'latin-1')
        print('Working on {}'.format(self.country_iso3))
        
        for idx, country in countries.iterrows():

            if not country['iso3'] == self.country_iso3: 

                continue   
            
            #define our country-specific parameters, including gid information
            iso3 = country['iso3']
            gid_region = country['gid_region']
            gid_level = 'GID_{}'.format(gid_region)
            
            #set the filename depending our preferred regional level
            large_countries = ['ARG', 'BRA', 'CHN', 'USA', 'DZA', 'IND', 'RUS']
            if country['iso3'] in large_countries:
                
                filename = 'regions_1_{}.shp'.format(iso3)
                gid_level = 'GID_1'

            else:

                filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
                gid_level = 'GID_{}'.format(gid_region)
            folder = os.path.join('data','processed', iso3, 'regions')
            
            #then load in our regions as a geodataframe
            path_regions = os.path.join(folder, filename)
            regions = gpd.read_file(path_regions, crs = 'epsg:4326')#[:2]
            
            for idx, region in regions.iterrows():

                #get our gid id for this region 
                #(which depends on the country-specific gid level)
                gid_id = region[gid_level]
                
                filename = 'ppp_2020_1km_Aggregated.tif'
                folder = os.path.join('data','processed', iso3, 'population', 'national')
                path_pop = os.path.join(folder, filename)
                hazard = rasterio.open(path_pop, 'r+')
                hazard.nodata = 255                      
                hazard.crs.from_epsg(4326)                

                geo = gpd.GeoDataFrame(gpd.GeoSeries(region.geometry))

                geo = geo.rename(columns = {0:'geometry'}).set_geometry('geometry')

                coords = [json.loads(geo.to_json())['features'][0]['geometry']] 

                out_img, out_transform = mask(hazard, coords, crop = True)

                out_meta = hazard.meta.copy()

                out_meta.update({'driver': 'GTiff', 'height': out_img.shape[1],
                                'width': out_img.shape[2], 'transform': out_transform,
                                'crs': 'epsg:4326'})

                filename_out = '{}.tif'.format(gid_id) 
                folder_out = os.path.join('data', 'processed', self.country_iso3, 'population', 'tiffs')

                if not os.path.exists(folder_out):

                    os.makedirs(folder_out)

                path_out = os.path.join(folder_out, filename_out)

                with rasterio.open(path_out, 'w', **out_meta) as dest:

                    dest.write(out_img)
            
            print('Processing complete for {}'.format(iso3))


    def pop_process_shapefiles(self):

        """
        This function process each of the population 
        raster layers to vector shapefiles
        """
        folder = os.path.join('data', 'processed', self.country_iso3, 'population', 'tiffs')

        for tifs in tqdm(os.listdir(folder), 
                         desc = 'Processing population shapefiles for {}...'.format(self.country_iso3)):
            try:
                if tifs.endswith('.tif'):

                    tifs = os.path.splitext(tifs)[0]

                    folder = os.path.join('data', 'processed', self.country_iso3, 'population', 'tiffs')
                    filename = tifs + '.tif'
                    
                    path_in = os.path.join(folder, filename)

                    folder = os.path.join('data', 'processed', self.country_iso3, 'population', 'shapefiles')
                    if not os.path.exists(folder):

                        os.mkdir(folder)
                        
                    filename = tifs + '.shp'
                    path_out = os.path.join(folder, filename)

                    with rasterio.open(path_in) as src:

                        affine = src.transform
                        array = src.read(1)

                        output = []

                        for vec in rasterio.features.shapes(array):

                            if vec[1] > 0 and not vec[1] == 255:

                                coordinates = [i for i in vec[0]['coordinates'][0]]

                                coords = []

                                for i in coordinates:

                                    x = i[0]
                                    y = i[1]

                                    x2, y2 = src.transform * (x, y)

                                    coords.append((x2, y2))

                                output.append({
                                    'type': vec[0]['type'],
                                    'geometry': {
                                        'type': 'Polygon',
                                        'coordinates': [coords],
                                    },
                                    'properties': {
                                        'value': vec[1],
                                    }
                                })

                    output = gpd.GeoDataFrame.from_features(output, crs = 'epsg:4326')
                    output.to_file(path_out, driver = 'ESRI Shapefile')

            except:
                pass

        return None


class PovertyProcess:
    """
    This class process the poverty raw data.
    """


    def __init__(self, csv_country, country_iso3, gid_region, poverty_shp):
        """
        A class constructor

        Arguments
        ---------
        csv_country : string
            Name of the country metadata file.
        country_iso3 : string
            Country iso3 to be processed.
        gid_region: string
            GID boundary spatial level to process
        poverty_shp: string
            Filename of the poverty vector layer
        """
        self.csv_country = csv_country
        self.country_iso3 = country_iso3
        self.gid_region = gid_region
        self.poverty_shp = poverty_shp

    def country_poverty(self):
        """
        This function generates a national poverty shapefile.
        """
        countries = pd.read_csv(self.csv_country, encoding = 'latin-1')
        large_countries = ['ARG', 'BRA', 'CHN', 'USA', 'DZA', 'IND', 'RUS']
        
        for idx, country in countries.iterrows():

            if not country['iso3'] == self.country_iso3: 

                continue   

            iso3 = country['iso3']
            if country['iso3'] in large_countries:

                region_name = 'regions_1_{}.shp'.format(iso3)
                filename_out = 'poverty_1_{}.shp'.format(iso3)

            else:

                gid_region = country['gid_region']
                region_name = 'regions_{}_{}.shp'.format(gid_region, iso3)
                filename_out = 'poverty_{}_{}.shp'.format(gid_region, iso3)

            filename_in = self.poverty_shp
            poverty_file_in = os.path.join(filename_in)

            #Load in the world poverty shapefile
            world_gdf = gpd.read_file(poverty_file_in, crs = 'epsg:4326')
                #set the filename depending our preferred regional level

            region_folder = os.path.join('data', 'processed', iso3, 'regions')
            
            #Load region name
            region_file = os.path.join(region_folder, region_name)
            mask_gdf = gpd.read_file(region_file)

            print('Pre-processing {} poverty data'.format(iso3))
            clipped_gdf = gpd.overlay(world_gdf, mask_gdf, how = 'intersection')

            folder_out = os.path.join('data', 'processed', iso3, 'poverty', 'national')

            if not os.path.exists(folder_out):

                os.makedirs(folder_out)

            path_out = os.path.join(folder_out, filename_out)

            clipped_gdf.to_file(path_out)

        return None
    

    def process_regional_poverty(self):
        """
        Function to process poverty of a single region 
        of an LMIC country.  
        """
        countries = pd.read_csv(self.csv_country, encoding = 'latin-1')

        iso3 = self.country_iso3
        print('Intersecting {} regional poverty datapoints'.format(iso3))
        for idx, country in countries.iterrows():

            if not country['iso3'] == iso3:

                continue

            iso3 = country['iso3']                 
            gid_region = country['gid_region']
            
            large_countries = ['ARG', 'BRA', 'CHN', 'USA', 'DZA', 'IND', 'RUS']

            if country['iso3'] in large_countries:
                
                filename = 'regions_1_{}.shp'.format(iso3)
                poverty_filename = 'poverty_1_{}.shp'.format(iso3) 
                gid_level = 'GID_1'

            else:

                filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
                poverty_filename = 'poverty_{}_{}.shp'.format(gid_region, iso3) 
                gid_level = 'GID_{}'.format(gid_region)

            #Load regional shapefile
            folder = os.path.join('data','processed', iso3, 'regions')
            path_regions = os.path.join(folder, filename)
            regions = gpd.read_file(path_regions, crs = 'epsg:4326')

            print('Processing regional {} poverty data'.format(iso3))
            #Load poverty shapefile
            for idx, region in regions.iterrows():

                gid_id = region[gid_level]
                folder= os.path.join(DATA_PROCESSED, iso3 , 'poverty', 'national')
                path_pov = os.path.join(folder, poverty_filename)

                gdf_pov = gpd.read_file(path_pov, crs = 'EPSG:4326')
                gdf_region = regions[regions[gid_level] == gid_id]

                try:

                    gdf_cov = gpd.overlay(gdf_region, gdf_pov, how = 'intersection')
                
                    filename = '{}.shp'.format(gid_id)
                    folder_out = os.path.join(BASE_PATH, 'processed', iso3, 'poverty', 'regions')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, filename)     
                    gdf_cov.to_file(path_out, crs = 'EPSG:4326')

                except: 

                    pass

        return None