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

class CoastProcess:
    """
    This class process the flood layers using the country boundary.
    """

    def __init__(self, csv_filename, country_iso3, flood_tiff):
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
            large_countries = ['BRA', 'CHN', 'USA', 'DZA', 'IND', 'RUS']
            if country['iso3'] in large_countries:
                
                filename = 'regions_1_{}.shp'.format(iso3)
                gid_level = 'GID_1'

            else:

                filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
                gid_level = 'GID_{}'.format(gid_region)
            filename = 'regions_{}_{}.shp'.format(gid_region, iso3)
            folder = os.path.join('data','processed', iso3, 'regions')
            
            #then load in our regions as a geodataframe
            path_regions = os.path.join(folder, filename)
            regions = gpd.read_file(path_regions, crs = 'epsg:4326')
            
            for idx, region in regions.iterrows():

                #get our gid id for this region 
                #(which depends on the country-specific gid level)
                gid_id = region[gid_level]
                gid_name = region['NAME_1']
                
                print('Working on {} coastal flooding layers'.format(gid_name))
                
                #let's load in our hazard layer
                filename = self.flood_tiff
                path_hazard = os.path.join(filename)
                hazard = rasterio.open(path_hazard, 'r+')
                hazard.nodata = 255                       
                hazard.crs.from_epsg(4326)                

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

                out_meta.update({'driver': 'GTiff', 'height': out_img.shape[1],
                                'width': out_img.shape[2], 'transform': out_transform,
                                'crs': 'epsg:4326'})

                #now we write out at the regional level
                filename_out = '{}.tif'.format(gid_id) 
                folder_out = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inuncoast', 'tifs')

                if not os.path.exists(folder_out):

                    os.makedirs(folder_out)

                path_out = os.path.join(folder_out, filename_out)

                with rasterio.open(path_out, 'w', ** out_meta) as dest:
                    dest.write(out_img)
            
            print('Processing complete for {}'.format(iso3))
        
        return None 

    def process_flood_shapefile(self):

        """
        This function process each of the tiff files into shapefiles
        """
        folder = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inuncoast', 'tifs')

        for tifs in tqdm(os.listdir(folder), 
                         desc = 'Processing flooding shapefiles for {}...'.format(self.country_iso3)):

            try:

                if tifs.endswith('.tif'):

                    tifs = os.path.splitext(tifs)[0]

                    folder = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inuncoast', 'tifs')
                    filename = tifs + '.tif'
                    
                    path_in = os.path.join(folder, filename)

                    folder = os.path.join('data', 'processed', self.country_iso3, 'hazards', 'inuncoast', 'shapefiles')
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