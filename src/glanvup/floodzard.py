import os                 
import json
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

class FloodProcess:
    """
    This class process the flood layers using the country boundary.
    """

    def __init__(self, csv_filename, country_iso3, flood_tiff, pop_csv):
        """
        A class constructor.

        Arguments
        ---------
        csv_filename : string
            Name of the country metadata file.
        country_iso3 : string
            Country iso3 to be processed.
        flood_tiff: string
            Filename of the tif flood raster layer
        """
        self.csv_filename = csv_filename
        self.country_iso3 = country_iso3
        self.flood_tiff = flood_tiff
        self.pop_csv = pop_csv

    def process_flood_tiff(self):
        """
        Pre-process flood layers.

        """
        countries = pd.read_csv(self.csv_filename, encoding = 'latin-1')
        
        for idx, country in countries.iterrows():

            if not country['iso3'] == self.country_iso3: 
                continue   
            
            #define our country-specific parameters, including gid information
            iso3 = country['iso3']
            gid_region = country['gid_region']
            gid_level = 'GID_{}'.format(gid_region)

            
            #set the filename depending our preferred regional level
            filename = "gadm_{}.shp".format(gid_region)
            folder = os.path.join('data','processed', iso3, 'regions')
            
            #then load in our regions as a geodataframe
            path_regions = os.path.join(folder, filename)
            regions = gpd.read_file(path_regions, crs = 'epsg:4326')#[:2]
            
            for idx, region in regions.iterrows():

                #get our gid id for this region 
                #(which depends on the country-specific gid level)
                gid_id = region[gid_level]
                
                print('----Working on {}'.format(gid_id))
                
                #let's load in our hazard layer
                filename = self.flood_tiff
                path_hazard = os.path.join('data','raw','flood_hazard', filename)
                hazard = rasterio.open(path_hazard, 'r+')
                hazard.nodata = 255                       #set the no data value
                hazard.crs.from_epsg(4326)                #set the crs

                #create a new gpd dataframe from our single region geometry
                geo = gpd.GeoDataFrame(gpd.GeoSeries(region.geometry))

                #this line sets geometry for resulting geodataframe
                geo = geo.rename(columns = {0:'geometry'}).set_geometry('geometry')

                #convert to json
                coords = [json.loads(geo.to_json())['features'][0]['geometry']] 
                
                #carry out the clip using our mask
                out_img, out_transform = mask(hazard, coords, crop = True)

                #update our metadata
                out_meta = hazard.meta.copy()

                out_meta.update({"driver": "GTiff", "height": out_img.shape[1],
                                "width": out_img.shape[2], "transform": out_transform,
                                "crs": 'epsg:4326'})

                #now we write out at the regional level
                filename_out = '{}.tif'.format(gid_id) #each regional file is named using the gid id
                folder_out = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inunriver', 'tifs')

                if not os.path.exists(folder_out):
                    os.makedirs(folder_out)

                path_out = os.path.join(folder_out, filename_out)

                with rasterio.open(path_out, "w", **out_meta) as dest:
                    dest.write(out_img)
            
            print('Processing complete for {}'.format(iso3))
        
        return None 

    def process_tif(self):

        """
        This function process each of the tif files into shapefiles
        """
        folder = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inunriver', 'tifs')

        for tifs in os.listdir(folder):
            try:
                if tifs.endswith('.tif'):
                    tifs = os.path.splitext(tifs)[0]

                    folder = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inunriver', 'tifs')
                    filename = tifs + '.tif'
                    
                    path_in = os.path.join(folder, filename)

                    folder = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inunriver', 'shapefiles')
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
    
    def pop_flood(self):
        """
        This function combines flooding shapefiles with population data
        and plots them to show the location of vulnerable areas. 
        """
        folder = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inunriver', 'shapefiles')

        combined_gdf = gpd.GeoDataFrame(crs = 'epsg:4326')

        for shapefiles in os.listdir(folder):
            
            if shapefiles.endswith('.shp'):
                
                filepath = os.path.join(folder, shapefiles)
                
                # Read the shapefile and add it to the combined dataframe
                gdf = gpd.read_file(filepath)
                combined_gdf = combined_gdf.append(gdf, ignore_index = True)
        
        return combined_gdf

    def flood_pop_merge(self):
        """
        This function merges the population data with the boundary data and then 
        performs a spatial intersection overlaying operation to determine the 
        number of vulnerable people in the flooded regions

        """
        # Import the population dataset
        data = pd.read_csv(self.pop_csv)
        
        # Import the previously processed boundaries dataset.
        folder = os.path.join('data', 'processed', self.country_iso3, 'regions')
        for shapefiles in os.listdir(folder):
            if shapefiles.endswith('.shp'):
                shp_in = os.path.join(folder, shapefiles)
                country_boundaries = gpd.read_file(shp_in)
                
                #merge the boundary dataset with population dataset and confirm the projection.
                
                pop_bound_flood = country_boundaries.merge(data, left_on = 'GID_1', right_on = 'GID_1')
        
        return pop_bound_flood

    def intersect_layers(self):

        """
        This function intersects two geospatial layers.
        """

        gdf1 = FloodProcess.flood_pop_merge(self)
        gdf2 = FloodProcess.pop_flood(self)

        print('Intersecting flood and population layers...')

        intersection_gdf = gpd.overlay(gdf2, gdf1, how = 'intersection')
        
        return intersection_gdf   

    def quantification(self):
        """
        Quantify the number of people vulnerable to riverine flooding
        """
        flood_gdf = FloodProcess.intersect_layers(self)

        # Select columns to use
        gdf = flood_gdf[['NAME_1_x', 'population', 'value', 'geometry']]

        # Calculate the area occupied by vulnerable people
        gdf['area'] = gdf.geometry.area
        gdf = gdf.drop(['geometry'], axis = 1)
        gdf[['scenario', 'period']] = ''
        
        for i in range(len(gdf)):
            scenarios = ['historical', 'rcp4p5','rcp8p5']
            periods = ['rp00100', 'rp01000']
            for scenario in scenarios:
                if scenario in self.flood_tiff:
                    gdf['scenario'].loc[i] = scenario
    
            for period in periods:
                if period in self.flood_tiff:
                    gdf['period'].loc[i] = period

        filename = '{}results.csv'.format(self.flood_tiff).replace('.tif', '_')
        
        folder = os.path.join('data', 'processed', self.country_iso3, 'csv_results')

        if not os.path.exists(folder):
            os.makedirs(folder)

        path_out = os.path.join(folder, filename)
        gdf.to_csv(path_out)

        return gdf
    
    def process_csvs(self):
        """
        This function concatenates all csv intersection results into a single file.
        """

        folder = os.path.join('data', 'processed', self.country_iso3, 'csv_results')

        # Get a list of all CSV files in the folder
        csv_files = [file for file in os.listdir(folder) if file.endswith('.csv')]

        # Initialize an empty DataFrame
        concatenated_data = pd.DataFrame()

        # Iterate through each CSV file
        print('Concatenating flooding scenario and period file results')
        for file in csv_files:

            # Read the CSV file into a DataFrame
            file_path = os.path.join(folder, file)
            df = pd.read_csv(file_path)

            # Concatenate the DataFrame with the existing data
            concatenated_data = pd.concat([concatenated_data, df], axis = 0, ignore_index = True, sort = False)
        
        concatenated_data.sort_values(by = 'NAME_1_x', inplace = True)

        hazard_type = self.flood_tiff.split('_')[0]
        country = self.country_iso3
        filename = '{}_{}_flooding_results.csv'.format(hazard_type, country)

        path_out = os.path.join(folder, filename)
        concatenated_data.to_csv(path_out)

        return concatenated_data