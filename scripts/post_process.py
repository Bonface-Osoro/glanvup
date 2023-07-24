import os
import pandas as pd
import configparser
import time
import warnings
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RESULTS = os.path.join(BASE_PATH, 'results')

asia = ['AFG', 'ARM', 'AZE', 'BHR', 'BGD', 'BTN', 'BRN', 'MMR', 'KHM', 
        'CHN', 'CXR', 'CCK', 'IOT', 'GEO', 'HKG', 'IND', 'IDN', 'IRN', 
        'IRQ', 'ISR', 'JPN', 'JOR', 'KAZ', 'PRK', 'KOR', 'KWT', 'KGZ', 
        'LAO', 'LBN', 'MAC', 'MYS', 'MDV', 'MNG', 'OMN', 'NPL', 'PAK', 
        'PSE', 'PHL', 'QAT', 'SAU', 'SGP', 'LKA', 'SYR', 'TWN', 'TJK', 
        'THA', 'TUR', 'TKM', 'ARE', 'UZB', 'VNM', 'YEM', 'TLS']

south_America = ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 
                 'PER', 'SUR', 'URY', 'VEN']

north_america = ['ATG', 'BHS', 'BRB', 'BLZ', 'CAN', 'CRI', 'CUB', 'DMA', 
                 'DOM', 'SLV', 'GTM', 'HTI', 'HND', 'JAM', 'MEX', 'NIC', 
                 'PAN', 'KNA', 'LCA', 'VCT', 'TTO', 'USA', 'ABW', 'AIA', 
                 'BMU', 'BES', 'VGB', 'CYM', 'CUB', 'CUW', 'DMA', 'DOM', 
                 'GRD', 'GLP', 'GRL', 'MTQ', 'MSR', 'PRI', 'BES', 'BES', 
                 'KNA', 'LCA', 'SPM', 'VCT', 'TTO', 'TCA', 'VIR']

africa = ['DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 
          'TCD', 'COM', 'COG', 'COD', 'DJI', 'EGY', 'GNQ', 'ERI', 'SWZ', 
          'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'CIV', 'KEN', 'LSO', 
          'LBR', 'LBY', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MAR', 'MOZ',
          'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 
          'ZAF', 'SSD', 'SDN', 'TZA', 'TGO', 'TUN', 'UGA', 'ZMB', 'ZWE']

europe = ['ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CYP', 
          'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'GEO', 'DEU', 'GRC', 'HUN', 
          'ISL', 'IRL', 'ITA', 'KAZ', 'KOS', 'LVA', 'LIE', 'LTU', 'LUX', 
          'MKD', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD', 'NOR', 'POL', 'PRT', 
          'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 
          'UKR', 'GBR', 'VAT', 'ALA', 'FRO', 'GIB', 'GGY', 'IMN', 'JEY', 
          'SJM']

oceania = ['ASM', 'AUS', 'COK', 'FJI', 'PYF', 'GUM', 'KIR', 'MHL', 'FSM', 
           'NRU', 'NCL', 'NZL', 'NIU', 'NFK', 'MNP', 'PLW', 'PNG', 'PCN', 
           'WSM', 'SLB', 'TKL', 'TON', 'TUV', 'UMI', 'VUT', 'WLF']

def global_average(metric):
    '''
    This function averages all the individual 
    vulnerable population into a single file. 
    It also averages the area under flooding risk.

    Parameters
    ----------
    iso3 : string
        Country ISO code
    metric : string
        Attribute being quantified. It can be area, 
        flood depth or population under flooding
        valid options are; 'area', 'flood' & 'population'
    '''

    isos = os.listdir(DATA_RESULTS)
    combined_df = pd.DataFrame()

    for iso3 in isos:

        csv_path = os.path.join(DATA_RESULTS, iso3, 'csv_files')

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
                    
                    fileout = '{}_{}_results.csv'.format(metric, metric)
                    folder_out = os.path.join(BASE_PATH, 'global_results')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    combined_df.to_csv(path_out, index = False)

    return None


global_average('population')
global_average('area')
global_average('flood')