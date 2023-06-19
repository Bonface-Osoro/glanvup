import configparser
import json
import os
import rasterio
import geopandas as gpd
import pandas as pd
from rasterio.mask import mask
from shapely.geometry import MultiPolygon
from tqdm import tqdm

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

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

        path = os.path.join('data', 'raw', 'gadm36_0.shp')

        countries = gpd.read_file(path)

        single_country = countries[countries.GID_0 == self.country_iso3].reset_index()

        single_country = single_country.copy()
        single_country['geometry'] = single_country.geometry.simplify(
            tolerance = 0.01, preserve_topology = True)
        
        single_country['geometry'] = single_country.apply(
            remove_small_shapes, axis = 1)
        
        glob_info_path = os.path.join(self.csv_country)
        load_glob_info = pd.read_csv(glob_info_path, encoding = 
                                     'ISO-8859-1', 
                                     keep_default_na = False)
        
        single_country = single_country.merge(
            load_glob_info, left_on = 'GID_0', 
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
        pop_tiff: string
            Filename of the population raster layer
        gid_region: string
            GID boundary spatial level to process
        region : string
            Region shapefile to process
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
        gid_level = 'GID_{}'.format(gid_region)

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

        with rasterio.open(path_out, "w", **out_meta) as dest:
            dest.write(out_img)

        return print('Population processing completed for {}'.format(iso3))
    

    def process_regional_population(self):
        """
        This function creates a regional composite population .tiff 
        using regional boundary files created in 
        process_regional_boundary function and national
        population files created in process_national_population
        function.
        """
        countries = pd.read_csv(self.csv_country, encoding = 'latin-1')
        
        for idx, country in countries.iterrows():

            if not country['iso3'] == self.country_iso3: 
                continue   
            
            #define our country-specific parameters, including gid information
            iso3 = country['iso3']
            gid_region = country['gid_region']
            gid_level = 'GID_{}'.format(gid_region)

            
            #set the filename depending our preferred regional level
            filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
            folder = os.path.join('data','processed', iso3, 'regions')
            
            #then load in our regions as a geodataframe
            path_regions = os.path.join(folder, filename)
            regions = gpd.read_file(path_regions, crs = 'epsg:4326')#[:2]
            
            for idx, region in regions.iterrows():

                #get our gid id for this region 
                #(which depends on the country-specific gid level)
                gid_id = region[gid_level]
                gid_name = region['NAME_1']
                
                print('Working on {}'.format(gid_name))
                
                #loading in national population file
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

                filename_out = '{}.tif'.format(gid_id) #each regional file is named using the gid id
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
        raster layers toi vector shapefiles
        """
        folder = os.path.join('data', 'processed', self.country_iso3, 'population', 'tiffs')

        for tifs in tqdm(os.listdir(folder), desc = 'Processing population shapefiles for {}...'.format(self.country_iso3)):
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


class WealthProcess:
    """
    This class process the LMIC country wealth data.
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


    def process_national_rwi(self):
        """

        Function to process relative wealth 
        of a single LMIC country.
        """
        iso3 = self.country_iso3
        filename = '{}_relative_wealth_index.csv'.format(iso3)
        path_rwi = os.path.join(BASE_PATH, 'raw', 'rwi', filename)

        if os.path.isfile(path_rwi):

            wealth = gpd.read_file(path_rwi, encoding = 'latin-1')

            #making long lat points into geometry column
            gdf = gpd.GeoDataFrame(wealth, geometry = gpd.points_from_xy(wealth.longitude, wealth.latitude), 
                                crs = 'EPSG:4326') 
            #setting path out
            filename_out = '{}_relative_wealth_index.shp'.format(iso3) #each regional file is named using the gid id
            folder_out = os.path.join(BASE_PATH, 'processed', iso3 , 'rwi', 'national')

            if not os.path.exists(folder_out):
                os.makedirs(folder_out)

            path_out = os.path.join(folder_out, filename_out)

            #saving new .csv to location
            gdf.to_file(path_out,crs = 'EPSG:4326')
        
        else:

            print('{}.relative wealth data not found. Skipping...'.format(iso3))

        return print('Relative wealth processing completed for {}'.format(iso3))
    

    def process_regional_rwi(self):
        """
        Function to process relative wealth 
        of a single region of an LMIC country.  
        """
        countries = pd.read_csv(self.csv_country, encoding = 'latin-1')

        iso3 = self.country_iso3

        for idx, country in countries.iterrows():
            if not country["iso3"] == iso3:
                continue

            iso3 = country['iso3']                 
            gid_region = country['gid_region']
            gid_level = 'GID_{}'.format(gid_region)

            filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
            folder = os.path.join('data','processed', iso3, 'regions')
            path_regions = os.path.join(folder, filename)
            regions = gpd.read_file(path_regions, crs = 'epsg:4326')

            for idx, region in regions.iterrows():
                gid_id = region[gid_level]

                #loading in gid level shapefile
                filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
                path_region = os.path.join(BASE_PATH, 'processed', iso3, 'regions', filename)
                gdf_region = gpd.read_file(path_region, crs = 'EPSG:4326')

                #loading in rwi info
                filename = '{}_relative_wealth_index.shp'.format(iso3) #each regional file is named using the gid id
                folder = os.path.join(BASE_PATH, 'processed', iso3 , 'rwi', 'national')
                path_rwi = os.path.join(folder, filename)

                if os.path.isfile(path_rwi):

                    gdf_rwi = gpd.read_file(path_rwi, crs = 'EPSG:4326')
                    gdf_region = gdf_region[gdf_region[gid_level] == gid_id]

                    print('Intersecting wealth data {}'.format(gid_id))

                    gdf_rwi = gpd.overlay(gdf_rwi, gdf_region, how = 'intersection')

                    filename = '{}.shp'.format(gid_id)
                    folder_out = os.path.join(BASE_PATH, 'processed', iso3, 'rwi', 'regions' )
                    if not os.path.exists(folder_out):
                        os.makedirs(folder_out)
                    path_out = os.path.join(folder_out, filename)

                    gdf_rwi.to_file(path_out, crs = 'EPSG:4326')

                else:

                    print('{} relative wealth data not found. Skipping...'.format(iso3))

        return print('Regional relative wealth processing completed for {}'.format(iso3))