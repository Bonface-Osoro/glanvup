"""
Process population for the whole world

Written by Osoro Bonface & Edward Oughton
May 2023
George Mason university, USA
"""

import os
import json
import rasterio
import warnings
import geopandas as gpd 
import numpy as np
import pandas as pd
from rasterio.mask import mask
from rasterstats import zonal_stats
from shapely.geometry import MultiPolygon
warnings.filterwarnings('ignore')

class GlobalPopulation:
    """
    This class calculates population for every country.
    """
    def __init__(self, csv_filename, country_iso3, gid_level, pop_tiff):
        """
        A class constructor.

        Arguments
        ---------
        csv_filename : string
            Name of the country metadata file.
        country_iso3 : string
            Country iso3 to be processed.
        boundary_data_path : string
            Location of the GADM boundary data.
        gid_level: string
            GID boundary spatial level to process
        country_shapefile: string
            Filename of the processed country shapefile
        pop_tiff: string
            Filename of the population raster layer
        """
        self.csv_filename = csv_filename
        self.country_iso3 = country_iso3
        self.gid_level = gid_level
        self.pop_tiff = pop_tiff
      
    def country_directory(self):
        """
        Create country folder and regions subfolder within it.

        Returns
        -------
        output : list
            List containing country ISO3 and gid_region
        """
        countries = pd.read_csv(self.csv_filename, encoding = 'latin-1')
    
        output = []
    
        for idx, country in countries.iterrows():
            
            if not country['iso3'] == self.country_iso3: #If the current country iso3 does not match the entered iso3...
                continue                            #continue in the loop to the next country
                
            iso3 = country['iso3']
            gid_region = country['gid_region']
            country_name = country['country']
            lowest = country['lowest']
            
            output.append(iso3)
            output.append(gid_region)
            output.append(lowest)
            
            country_folder_path = os.path.join('data', 'processed', iso3) #Create folder called "processed" to store
            if not os.path.exists(country_folder_path):                   #country folder
                os.makedirs(country_folder_path)                          #Onle create folder if it doest exist already
                
            regions_folder_path = os.path.join('data', 'processed', iso3, 'regions') #Create regions folder within
            if not os.path.exists(regions_folder_path):
                os.makedirs(regions_folder_path)
                
            print('processing {}'.format(country_name))      
    
        return output

    def country_boundary(self):
        """
        Process country shapefile.
            
        Returns
        -------
        none  
        """
        
        iso3 = GlobalPopulation.country_directory(self)[0]
        gid_region = GlobalPopulation.country_directory(self)[1]

        filename = 'gadm36_{}.shp'.format(gid_region)
        boundary_data = os.path.join('data', 'raw', filename)

        global_boundaries = gpd.read_file(boundary_data)
        
        country_boundaries = global_boundaries[global_boundaries['GID_0'] == iso3]
        gid_level_name = country_boundaries['NAME_1']
        
        filename = 'gadm_{}.shp'.format(gid_region)
        path_out = os.path.join('data', 'processed', iso3, 'regions', filename)
        country_boundaries.to_file(path_out)
        
        print('processing {}'.format(gid_level_name))
        
        return None
    
    def process_population_tif(self):
        """
        Process population layer.
            
        Returns
        -------
        output: dictionary.
            Dictionary containing the country population and grid level
        """
        output = []

        gid_region = GlobalPopulation.country_directory(self)[1]
        
        filename = 'gadm_{}.shp'.format(gid_region)
        country_shapefile = os.path.join('data', 'processed', self.country_iso3, 'regions', filename)

        boundaries = gpd.read_file(country_shapefile, crs = 'epsg:4326') 

        for idx, boundary in boundaries.iterrows():
            
            print('Working on {}'.format(boundary['NAME_1']))
            
            with rasterio.open(self.pop_tiff) as src:
                
                affine = src.transform
                array = src.read(1)
                array[array <= 0] = 0
                
                population = [i['sum'] for i in zonal_stats(
                    boundary['geometry'], array, nodata = 255,
                    stats = ['sum'], affine = affine)][0]
                output.append({
                    'NAME_1': boundary['NAME_1'],
                    'GID_1': boundary[self.gid_level],
                    'population': population
                })
                
        return output