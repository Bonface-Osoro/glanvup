import os
import configparser
import warnings
import pandas as pd
from glanvup.continents import asia, south_America, north_america, africa, europe, oceania 
from glanvup.continents import east_asia_pacific, europe_central_asia, latin_and_caribbean
from glanvup.continents import middle_north_africa, sub_saharan_africa, north_america_reg
from glanvup.continents import south_asia, low_income, low_middle, upper_income, high_income
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
        valid options are; 'area', 'depth' & 'population'
    '''

    isos = os.listdir(DATA_RESULTS)
    combined_df = pd.DataFrame()

    for iso3 in isos:

        csv_path = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

        for root, _, files in os.walk(csv_path):

            for file in files:

                if file.endswith('_{}_{}_average.csv'.format(hazard, metric)):

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


def global_vulnerable(metric, hazard):
    '''
    This function averages all the individual 
    vulnerable population into a single file. 
    It also classifies the individual countries 
    into specific continnets, regions and income group.

    Parameters
    ----------
    metric : string
        Attribute being quantified. It can be area, 
        flood depth or population under flooding
        valid options are; 'area', 'depth' & 'population'

    hazard : string
        Hazard quantified: i.e `riverine`, `coastal`
        or `tropical`.
    '''

    isos = os.listdir(DATA_RESULTS)

    combined_df = pd.DataFrame()

    for iso3 in isos:
        
        print('Processing continent, region and income for {} {} csv file'.format(iso3, hazard))
        csv_path = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

        for root, _, files in os.walk(csv_path):

            for file in files:

                if file.endswith('{}_{}_average.csv'.format(hazard, metric)):

                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    
                    columns_to_round = ['country', 'scenario', 'period']
                    df[columns_to_round] = df[columns_to_round].round(4)
                    df[['continent', 'region', 'income']] = ''

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

                    for i in range(len(df)):

                        if iso3 in sub_saharan_africa:

                            df['region'].loc[i] = 'SSA'
                            
                        elif iso3 in east_asia_pacific:

                            df['region'].loc[i] = 'EAP'

                        elif iso3 in europe_central_asia:

                            df['region'].loc[i] = 'ECA'

                        elif iso3 in latin_and_caribbean:

                            df['region'].loc[i] = 'LAC'

                        elif iso3 in middle_north_africa:

                            df['region'].loc[i] = 'MENA'

                        elif iso3 in north_america_reg:

                            df['region'].loc[i] = 'NA'

                        else: 

                            df['region'].loc[i] = 'SA'

                    for i in range(len(df)):

                        if iso3 in low_income:

                            df['income'].loc[i] = 'LIC'

                        elif iso3 in low_middle:

                            df['income'].loc[i] = 'LMC'

                        elif iso3 in upper_income:

                            df['income'].loc[i] = 'UMC'

                        else: 

                            df['income'].loc[i] = 'HIC'
                    df.rename(columns = {'country':'iso3'}, inplace = True)
                    combined_df = pd.concat([combined_df, df], ignore_index = True)
                    
                    fileout = 'vulnerable_{}_{}_results.csv'.format(hazard, metric)
                    folder_out = os.path.join(BASE_PATH, 'global_results')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    combined_df.to_csv(path_out, index = False)

    return None


def global_unconnected():
    '''
    This function merges all the individual 
    unconnected population into a single file. 
    It also classifies the individual countries 
    into specific continents, regions and income group.

    '''

    isos = os.listdir(DATA_RESULTS)
    combined_df = pd.DataFrame()

    for iso3 in isos:

        print('Processing continent, region and income for {} unconnected csv file'.format(iso3))

        try:

            csv_path = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files')

            for root, _, files in os.walk(csv_path):

                for file in files:

                    if file.endswith('_cellphone_average.csv'):

                        file_path = os.path.join(root, file)
                        df = pd.read_csv(file_path)

                        df[['iso3', 'continent', 'region', 'income']] = ''

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

                        for i in range(len(df)):

                            if iso3 in sub_saharan_africa:

                                df['region'].loc[i] = 'SSA'

                            elif iso3 in east_asia_pacific:

                                df['region'].loc[i] = 'EAP'

                            elif iso3 in europe_central_asia:

                                df['region'].loc[i] = 'ECA'

                            elif iso3 in latin_and_caribbean:

                                df['region'].loc[i] = 'LAC'

                            elif iso3 in middle_north_africa:

                                df['region'].loc[i] = 'MENA'

                            elif iso3 in north_america_reg:

                                df['region'].loc[i] = 'NA'

                            else: 

                                df['region'].loc[i] = 'SA'

                        for i in range(len(df)):

                            if iso3 in low_income:

                                df['income'].loc[i] = 'LIC'

                            elif iso3 in low_middle:

                                df['income'].loc[i] = 'LMC'

                            else: 

                                df['income'].loc[i] = 'UMC'

                        for i in range(len(df)):

                            df['iso3'].loc[i] = iso3

                            df = df[['iso3', 'value', 'technology', 'region', 'income', 'continent']]

                        combined_df = pd.concat([combined_df, df], ignore_index = True)
                        
                        fileout = 'unconnected_global_results.csv'.format()
                        folder_out = os.path.join(BASE_PATH, 'global_results')

                        if not os.path.exists(folder_out):

                            os.makedirs(folder_out)

                        path_out = os.path.join(folder_out, fileout)
                        combined_df.to_csv(path_out, index = False)
        except:

            pass

    return None


def globally_poor():
    '''
    This function averages all the individual 
    unconnected population into a single file. 
    It also classifies the individual countries 
    into specific continnets, regions and income group.

    '''

    isos = os.listdir(DATA_RESULTS)
    combined_df = pd.DataFrame()

    for iso3 in isos:
        
        print('Processing continent, region and income information for {} poverty csv file'.format(iso3))

        try:

            csv_path = os.path.join(DATA_RESULTS, iso3, 'povert_inline_csv_files')

            for root, _, files in os.walk(csv_path):

                for file in files:

                    if file.endswith('.csv'):

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

                        for i in range(len(df)):

                            if iso3 in sub_saharan_africa:

                                df['region'].loc[i] = 'SSA'

                            elif iso3 in east_asia_pacific:

                                df['region'].loc[i] = 'EAP'

                            elif iso3 in europe_central_asia:

                                df['region'].loc[i] = 'ECA'

                            elif iso3 in latin_and_caribbean:

                                df['region'].loc[i] = 'LAC'

                            elif iso3 in middle_north_africa:

                                df['region'].loc[i] = 'MENA'

                            elif iso3 in north_america_reg:

                                df['region'].loc[i] = 'NA'

                            else: 

                                df['region'].loc[i] = 'SA'

                        for i in range(len(df)):

                            if iso3 in low_income:

                                df['income'].loc[i] = 'LIC'

                            elif iso3 in low_middle:

                                df['income'].loc[i] = 'LMC'

                            elif iso3 in upper_income:

                                df['income'].loc[i] = 'UMC'

                            else: 

                                df['income'].loc[i] = 'HIC'

                        df['poverty_range'] = ''

                        for i in range(len(df)):

                            if df['rwi'].loc[i] <= 0:

                                df['poverty_range'].loc[i] = '< 0'

                            elif df['rwi'].loc[i] >= 0 and df['rwi'].loc[i] <= 0.5:

                                df['poverty_range'].loc[i] = '0 - 0.5'

                            else:

                                df['poverty_range'].loc[i] = '> 0.5'
                
                        combined_df = pd.concat([combined_df, df], ignore_index = True)
                        
                        fileout = 'poverty_inline_global_results.csv'.format()
                        folder_out = os.path.join(BASE_PATH, 'global_results')

                        if not os.path.exists(folder_out):

                            os.makedirs(folder_out)

                        path_out = os.path.join(folder_out, fileout)
                        combined_df.to_csv(path_out, index = False)
        except:
            pass

    return None


if __name__ == '__main__':
    
    #globally_poor()
    #global_unconnected()
    hazards = ['coastal']

    for hazard in hazards:

        #global_average('population', hazard)
        #global_average('area', hazard)
        global_vulnerable('depth', 'coastal')
        global_vulnerable('area', 'coastal')
        global_vulnerable('population', 'coastal')