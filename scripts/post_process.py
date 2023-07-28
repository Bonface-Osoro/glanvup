import os
import pandas as pd
import configparser
import time
import shutil
import warnings
from glanvup.continents import asia, south_America, north_america, africa, europe 
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RESULTS = os.path.join(BASE_PATH, 'results')

def global_average(metric, hazard):
    '''
    This function averages all the individual 
    vulnerable population into a single file. 
    It also averages the area under flooding risk.

    Parameters
    ----------
    hazard : string
        Hazard quantified: i.e `riverine`, `coastal`
        or `tropical`.
    metric : string
        Attribute being quantified. It can be area, 
        flood depth or population under flooding
        valid options are; 'area', 'flood' & 'population'
    '''

    isos = os.listdir(DATA_RESULTS)
    combined_df = pd.DataFrame()

    for iso3 in isos:

        csv_path = os.path.join(DATA_RESULTS, iso3, '{}_csv_files'.format(hazard))

        # Iterate over the folders
        for root, _, files in os.walk(csv_path):

            for file in files:

                if file.endswith('_{}_average.csv'.format(metric)):

                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    df['continent'] = ''

                    for i in range(len(df)):
                        if iso3 in asia:

                            df['continent'].loc[i] = 'Asia'

                        elif iso3 in africa:

                            df['continent'].loc[i] = 'Africa'

                        elif iso3 in south_America:

                            df['continent'].loc[i] = 'South America'

                        elif iso3 in north_america:

                            df['continent'].loc[i] = 'North America'

                        elif iso3 in europe:

                            df['continent'].loc[i] = 'Europe'

                        elif iso3 in oceania:

                            df['continent'].loc[i] = 'Oceania'

                        else:

                            df['continent'].loc[i] = 'Others'

            
                    combined_df = pd.concat([combined_df, df], ignore_index = True)
                    
                    fileout = '{}_{}_results.csv'.format(hazard, metric)
                    folder_out = os.path.join(BASE_PATH, 'global_results')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    combined_df.to_csv(path_out, index = False)

    return None


if __name__ == '__main__':

    hazards = ['riverine', 'coastal']

    for hazard in hazards:

        global_average('population', hazard)
        global_average('area', hazard)
        global_average('flood', hazard)