import os
import time
import pandas as pd
import geopandas as gpd
import configparser
from glanvup.rizard import FloodProcess
from glanvup.intersections import IntersectLayers
from glanvup.continents import asia, south_America, north_america, africa, europe, oceania 
from glanvup.continents import east_asia_pacific, europe_central_asia, latin_and_caribbean
from glanvup.continents import middle_north_africa, sub_saharan_africa, north_america_reg
from glanvup.continents import south_asia, low_income, low_middle, upper_income, high_income
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))

BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')
DATA_RESULTS = os.path.join(BASE_PATH, 'results')

def generate_unconnected_csv(intersect_folder, iso3):
    """
    This function generate a single 
    csv file of unconnected population 
    for an individual country  
    by cellphone technology.
    
    Parameters
    ----------
    intersect_folder : string
        Path of the folder containing 
        intersected shapefiles
    iso3 : string
        Country ISO3 code
    """
    
    print('processing unconnected cellphone {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)

            shapefile[['iso3', 'region', 'income', 'technology']] = ''
            technologies = ['GSM', '3G', '4G']

            for i in range(len(shapefile)):
                
                for technology in technologies:
                    
                    if technology in file_name:

                        shapefile['technology'].loc[i] = technology

                shapefile['iso3'].loc[i] = iso3 

            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area      
            shapefile = shapefile[['iso3', 'value','technology', 'region', 'income']]  
            merged_shapefile = pd.concat([merged_shapefile, shapefile], ignore_index = True)       
    
    fileout = '{}_unconnected_results.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def generate_cell_summation(iso3):
    """
    This function calculates the total number of unconected 
    people by cellphone technology for each country.

    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    """

    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    path_in = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files', 
        '{}_unconnected_results.csv'.format(iso3))
    
    df = pd.read_csv(path_in)

    print('Summing cellphone numbers for {}'.format(iso3))
    cellphone = df.groupby(['iso3', 'technology'])['value'].sum()

    fileout = '{}_cellphone_total.csv'.format(iso3)
    folder_out = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    cellphone.to_csv(path_out)
    
    return print('Summation completed for {}'.format(iso3))


def global_unconnected():
    '''
    This function merges all the individual 
    unconnected population into a single file. 
    It also classifies the individual countries 
    into specific continents, regions and income group.

    '''
    print('Aggregating global data of the unconnected population')
    isos = os.listdir(DATA_RESULTS)
    combined_df = pd.DataFrame()

    for iso3 in isos:

        try:

            csv_path = os.path.join(DATA_RESULTS, iso3, 'unconnected_csv_files')

            for root, _, files in os.walk(csv_path):

                for file in files:

                    if file.endswith('_cellphone_total.csv'):

                        file_path = os.path.join(root, file)
                        df = pd.read_csv(file_path)

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

                            else: 

                                df['income'].loc[i] = 'UMC'

                        for i in range(len(df)):

                            df['iso3'].loc[i] = iso3

                            df = df[['iso3', 'value', 'technology', 'region', 'income', 'continent']]

                        combined_df = pd.concat([combined_df, df], ignore_index = True)
                        
                        fileout = 'a_unconnected_global_results.csv'.format()
                        folder_out = os.path.join(BASE_PATH, 'global_results')

                        if not os.path.exists(folder_out):

                            os.makedirs(folder_out)

                        path_out = os.path.join(folder_out, fileout)
                        combined_df.to_csv(path_out, index = False)
        except:

            pass

    return None


def generate_poverty_csv(intersect_folder, iso3):
    """
    This function generate a single 
    csv file of the people living 
    below the poverty level 
    for an individual country  
    by cellphone technology.
    
    Parameters
    ----------
    intersect_folder : string
        Path of the folder containing 
        intersected shapefiles
    iso3 : string
        Country ISO3 code
    """
    
    print('Generating poverty in-line population {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)

            shapefile[['iso3', 'region', 'income',]] = ''

            for i in range(len(shapefile)):

                shapefile['iso3'].loc[i] = iso3
                shapefile['value'] = shapefile['value'].round(2)
            
            shapefile = shapefile[['iso3', 'value', 'rwi', 'region', 'income']]     

            merged_shapefile = pd.concat([merged_shapefile, shapefile], ignore_index = True)       
    
    fileout = '{}_poverty_inline_results.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'povert_inline_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
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
                        
                        fileout = 'b_poverty_inline_global_results.csv'.format()
                        folder_out = os.path.join(BASE_PATH, 'global_results')

                        if not os.path.exists(folder_out):

                            os.makedirs(folder_out)

                        path_out = os.path.join(folder_out, fileout)
                        combined_df.to_csv(path_out, index = False)
        except:
            
            pass

    return None


def riv_vulnerable_csv(iso3):
    """
    This function generate a single csv file of 
    vulnerable population to riverine flooding 
    for an individual country by climatic scenario 
    and period.
    
    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    """
    print('processing vulnerable population to riverine flooding {} csv'.format(iso3))
    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    intersect_folder = os.path.join(BASE_PATH, 'results', iso3, 'vul_river_hazard')
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)
            
            shapefile[['iso3', 'scenario', 'period', 'continent', 'region', 'income']] = ''
            scenarios = ['historical', 'rcp4p5', 'rcp8p5']
            periods = ['rp00100', 'rp01000']

            for i in range(len(shapefile)):

                shapefile['iso3'].loc[i] = iso3
                for scenario in scenarios:

                    if scenario in file_name:

                        shapefile['scenario'].loc[i] = scenario

                for period in periods:

                    if period in file_name:

                        shapefile['period'].loc[i] = period
            
            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area
            shapefile = shapefile[['iso3', 'value_1', 'value_2', 'period', 'scenario', 'area',
                                   'continent', 'region', 'income']]
            merged_shapefile = pd.concat([merged_shapefile, shapefile], ignore_index = True)           

    fileout = '{}_vulnerable_riverine.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def coast_vulnerable_csv(iso3):
    """
    This function generate a single csv file of 
    vulnerable population to coastal flooding 
    for an individual country by climatic scenario 
    and period.
    
    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    """
    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    intersect_folder = os.path.join(BASE_PATH, 'results', iso3, 'vul_coast_hazard')
    print('processing vulnerable population to coastal flooding {} csv'.format(iso3))
    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)
            
            shapefile[['iso3', 'scenario', 'period', 'continent', 
                       'region', 'income']] = ''
            scenarios = ['historical', 'rcp4p5', 'rcp8p5']
            periods = ['rp0100', 'rp1000']

            for i in range(len(shapefile)):

                shapefile['iso3'].loc[i] = iso3
                for scenario in scenarios:

                    if scenario in file_name:

                        shapefile['scenario'].loc[i] = scenario

                for period in periods:

                    if period in file_name:

                        shapefile['period'].loc[i] = period
            
            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area

            shapefile = shapefile[['iso3', 'value_1', 'value_2', 'period', 'scenario', 
                                   'area', 'continent', 'region', 'income']]

            merged_shapefile = pd.concat([merged_shapefile, 
                                          shapefile], 
                                          ignore_index = True)           

    fileout = '{}_vulnerable_coastal.csv'.format(iso3, merged_shapefile).replace('shp', '_')
    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def sum_hazards(iso3, hazard):
    """
    This function calculates the total number of people 
    vulnerable to flooding, the area they occupy and the
    average inundation depth of the floods. It also 
    regenerates the aggregate results in the previous function
    by cellphone technology.

    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    hazard : string
        Hazard quantified: i.e `riverine`, `coastal`
        or `tropical`.
    """

    DATA_RESULTS = os.path.join(BASE_PATH, 'results')
    path_in = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files', 
        '{}_vulnerable_{}.csv'.format(iso3, hazard))
    
    df = pd.read_csv(path_in)
    
    print('Summing {} data for {}'.format(hazard, iso3))

    flood = df.groupby(['iso3', 'scenario', 'period'])['value_2'].mean()
    
    population = df.groupby(['iso3', 'scenario', 'period'])['value_1'].sum()
    
    areas = df.groupby(['iso3', 'scenario', 'period'])['area'].sum()

    fileout = '{}_{}_depth_average_total.csv'.format(iso3, hazard)
    fileout_2 = '{}_{}_population_total.csv'.format(iso3, hazard)
    fileout_3 = '{}_{}_area_total.csv'.format(iso3, hazard)
    fileout_4 = '{}_{}_aggregated_results.csv'.format(iso3, hazard)

    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)
    path_out_2 = os.path.join(folder_out, fileout_2)
    path_out_3 = os.path.join(folder_out, fileout_3)
    path_out_4 = os.path.join(folder_out, fileout_4)

    flood.to_csv(path_out)
    population.to_csv(path_out_2)
    areas.to_csv(path_out_3)
    df.to_csv(path_out_4)
    
    return print('Summing completed for {}'.format(iso3))


def global_hazard_summation(metric, hazard):
    '''
    This function sums all the individual 
    vulnerable population into a single file. 
    It also averages the inundation flooding depth.

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
    print('Aggregating global {} data of population vulnerable to {} flooding'.format(metric, hazard))
    
    for iso3 in isos:

        csv_path = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

        for root, _, files in os.walk(csv_path):

            for file in files:

                if file.endswith('_{}_{}_total.csv'.format(hazard, metric)):

                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
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

                    combined_df = pd.concat([combined_df, df], ignore_index = True)
                    
                    fileout = 'c_{}_{}_results.csv'.format(hazard, metric)
                    folder_out = os.path.join(BASE_PATH, 'global_results')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    combined_df.to_csv(path_out, index = False)

    return None


def gen_agg_hazard_cov_csv(iso3, hazard):
    """
    This function generate a single 
    csv file of unconnected and vulnerable 
    population to riverine flooding for an 
    individual country by climate hazard 
    scenario and return period.
    
    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    hazard : string
        Hazard quantified: i.e `riverine`, `coastal`
        or `tropical`.
    """
    DATA_RESULTS = os.path.join(BASE_PATH, 'results')

    if hazard == 'riverine':
        print('Processing {} {} csv'.format(iso3, hazard))
        intersect_folder = os.path.join(BASE_PATH, 'results', iso3, 'cov_rizard')

    else:

        print('Processing {} {} csv'.format(iso3, hazard))
        intersect_folder = os.path.join(BASE_PATH, 'results', iso3, 'cov_cozard')

    merged_shapefile = gpd.GeoDataFrame()

    for file_name in os.listdir(intersect_folder):

        if file_name.endswith('.shp'):

            file_path = os.path.join(intersect_folder, file_name)
            shapefile = gpd.read_file(file_path)

            shapefile[['iso3', 'scenario', 'period', 'technology']] = ''
            scenarios = ['historical', 'rcp4p5','rcp8p5']
            periods = ['rp00100', 'rp0100', 'rp1000', 'rp01000']
            technologies = ['GSM', '3G', '4G']

            for i in range(len(shapefile)):

                for scenario in scenarios:

                    if scenario in file_name:

                        shapefile['scenario'].loc[i] = scenario

                for period in periods:

                    if period in file_name:

                        shapefile['period'].loc[i] = period
                
                for technology in technologies:
                    
                    if technology in file_name:

                        shapefile['technology'].loc[i] = technology

                shapefile['iso3'].loc[i] = iso3

            shapefile = shapefile[['iso3', 'value_1', 
                                'value_2', 'period', 'scenario', 
                                'technology', 'geometry']]

            shapefile = shapefile.to_crs(crs = 3857) 
            shapefile['area'] = shapefile.geometry.area
            shapefile = shapefile.drop(['geometry'], axis = 1)

            merged_shapefile = pd.concat([merged_shapefile, 
                                        shapefile], 
                                        ignore_index = True)           

    fileout = '{}_{}_unconnected_aggregated_results.csv'.format(iso3, hazard)
    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    merged_shapefile.to_csv(path_out, index = False)
    
    return None


def gen_sum_hazard_cov(iso3, hazard):
    """
    This function calculates the total number of unconnected 
    people vulnerable to hazards, the area they occupy and the
    average inundation depth of the floods. It also regenerates 
    the aggregate results by cellphone technology for each country.

    Parameters
    ----------
    iso3 : string
        Country ISO3 code
    hazard : string
        Hazard quantified: i.e `riverine`, `coastal`
        or `tropical`.
    """

    path_in = os.path.join(
        DATA_RESULTS, iso3, 'vulnerable_csv_files', 
        '{}_{}_unconnected_aggregated_results.csv'.format(iso3, hazard))
    
    df = pd.read_csv(path_in)
    
    print('Summing coverage and {} {} flooding data'.format(iso3, hazard))

    df = df.fillna('GSM')

    flood = df.groupby(['iso3', 'scenario', 'technology',
                        'period'])['value_2'].mean()
    
    population = df.groupby(['iso3', 'scenario', 'technology',
                             'period'])['value_1'].sum()
    
    areas = df.groupby(['iso3', 'scenario', 'technology',
                        'period'])['area'].sum()

    fileout = '{}_{}_depth_unconnected_total.csv'.format(iso3, hazard)
    fileout_2 = '{}_{}_population_unconnected_total.csv'.format(iso3, hazard)
    fileout_3 = '{}_{}_area_unconnected_total.csv'.format(iso3, hazard)
    fileout_4 = '{}_{}_unconnected_aggregated_results.csv'.format(iso3, hazard)

    folder_out = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)
    path_out_2 = os.path.join(folder_out, fileout_2)
    path_out_3 = os.path.join(folder_out, fileout_3)
    path_out_4 = os.path.join(folder_out, fileout_4)

    flood.to_csv(path_out)
    population.to_csv(path_out_2)
    areas.to_csv(path_out_3)
    df.to_csv(path_out_4)
    
    return None


def global_cov_haz_summation(metric, hazard):
    '''
    This function averages all the individual 
    unconnceted vulnerable population to hazards 
    into a single file. It also classifies the 
    individual countries into specific continnets, 
    regions and income group.

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
    print('Aggregating global {} data of unconnected population vulnerable to {} flooding'.format(metric, hazard))
    isos = os.listdir(DATA_RESULTS)

    combined_df = pd.DataFrame()

    for iso3 in isos:
        
        csv_path = os.path.join(DATA_RESULTS, iso3, 'vulnerable_csv_files')

        for root, _, files in os.walk(csv_path):

            for file in files:

                if file.endswith('{}_{}_unconnected_total.csv'.format(hazard, metric)):

                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    
                    columns_to_round = ['iso3', 'scenario', 'period']
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
                    
                    combined_df = pd.concat([combined_df, df], ignore_index = True)
                    
                    fileout = 'd_unconnected_{}_{}_results.csv'.format(hazard, metric)
                    folder_out = os.path.join(BASE_PATH, 'global_results')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    combined_df.to_csv(path_out, index = False)

    return None


if __name__ == '__main__':

    isos = os.listdir(DATA_RESULTS)
    isos = ['IDN']
    for iso in isos:

        try:

            ######### UNCONNECTED POPULATION #########
            folder = os.path.join( DATA_RESULTS, iso, 'pop_unconnected')
            #generate_unconnected_csv(folder, iso)
            #generate_cell_summation(iso)

            ######### POVERTY IN-LINE POPULATION #########
            #folder = os.path.join(DATA_RESULTS, iso, 'poor_population')
            #generate_poverty_csv(folder, iso)

            ######### VULNERABLE POPULATION TO RIVERINE FLOODING #########
            #riv_vulnerable_csv(iso)
            #sum_hazards(iso, 'riverine')

            ######### VULNERABLE POPULATION TO COASTAL FLOODING #########
            #coast_vulnerable_csv(iso)
            #sum_hazards(iso, 'coastal')

            ## UNCONNECTED & VULNERABLE POPULATION TO HAZARDS ##
            #gen_agg_hazard_cov_csv(iso, 'riverine')
            #gen_agg_hazard_cov_csv(iso, 'coastal')
            #gen_sum_hazard_cov(iso, 'riverine')
            #gen_sum_hazard_cov(iso, 'coastal')

        except:

            pass
    
    ## AGGREGATE GLOBAL UNCONNECTED POPULATION ##
    #global_unconnected()

    ## AGGREGATE GLOBAL POVERTY IN-LINE POPULATION ##
    #globally_poor()

    ## AGGREGATE GLOBAL POPULATION VULNERABLE TO NATURAL HAZARDS ##
    #global_hazard_summation('area', 'riverine')
    #global_hazard_summation('population', 'riverine')
    global_hazard_summation('area', 'coastal')
    global_hazard_summation('population', 'coastal')

    ## AGGREGATE GLOBAL UNCONNECTED POPULATION VULNERABLE TO NATURAL HAZARDS ##
    #global_cov_haz_summation('area', 'riverine')
    #global_cov_haz_summation('population', 'riverine')
    global_cov_haz_summation('area', 'coastal')
    global_cov_haz_summation('population', 'coastal')