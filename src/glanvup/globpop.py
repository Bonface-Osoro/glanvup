"""
Process population for the whole world

Written by Osoro Bonface & Edward Oughton
May 2023
George Mason university, USA
"""

import os
import numpy as np
import pandas as pd


class GlobalPopulation:
    """
    This class calculates population for every country.
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
            
            output.append(iso3)
            output.append(gid_region)
            
            country_folder_path = os.path.join('data', 'processed', iso3) #Create folder called "processed" to store
            if not os.path.exists(country_folder_path):                   #country folder
                os.makedirs(country_folder_path)                          #Onle create folder if it doest exist already
                
            regions_folder_path = os.path.join('data', 'processed', iso3, 'regions') #Create regions folder within
            if not os.path.exists(regions_folder_path):
                os.makedirs(regions_folder_path)
                
            print('processing {}'.format(country_name))      
    
        return output