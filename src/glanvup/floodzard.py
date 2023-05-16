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
from rasterstats import zonal_stats
from shapely.geometry import MultiPolygon
warnings.filterwarnings('ignore')

class FloodProcess:
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