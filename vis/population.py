import configparser
import os 
import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot



def plot_population(country_boundaries, csv_data, gid_level, iso3):
    """
    Plots the country's population at sub-region level.
    
    Parameters
    ----------
    country_boundaries : string
        Name of the country boundary .shp file
    csv_data : string
        Name of the csv file containing the population data
        at sub-regional level
    gid_level : string
        Name of the GID level
    country_iso3 = string
        ISO3 of the country
    
    Return
    ------
    fig : python object
        A map of population distribution. 
    """
    boundaries = country_boundaries.merge(csv_data, left_on = 'GID_0', #merge our population data onto our boundaries
                                  right_on = gid_level)
    
    bins = [-1e6,5000, 10000, 15000, 30000, 40000, 50000,        #define value bins and then labels for each one
            60000, 70000, 80000, 90000, 500000]
    labels = ['<300k', '300-320k','320-340k','340-360k','360-380k', '400-420k', 
              '420-440k', '440-460k', '460-480k', '480-500k', '500-520k']
     
    boundaries['bin'] = pd.cut(                                   #create a new variable with our bin labels
        boundaries['population'], 
        bins = bins,
        labels = labels
    )   
    
    sns.set(font_scale = 0.9)                                     #open a new seaborn figure
    fig, ax = plt.subplots(1, 1, figsize = (8, 8))

    base = boundaries.plot(column = 'bin', ax = ax,               #now plot our data using pandas plot
                           cmap = 'copper', linewidth = 0, 
                           legend = True, antialiased = False)
    #allocate a plot title 
    n = len(boundaries)
    name = 'DRC Population by Sub-Region(n={})'.format(n)
    fig.suptitle(name)
    
    path = os.path.join('data', 'processed', iso3, 'drc_population.png')
    fig.savefig(path)
    plt.close(fig)

    return fig

#import our boundaries data
filename = 'gadm_1.shp'.format(1)
path_in = os.path.join('data', 'processed', 'COD', 'regions', filename) 

filename2 = 'population.csv'
path_2 = os.path.join('data', 'processed', 'COD', filename2) 
data = pd.read_csv(path_2)

country_boundaries = gpd.read_file(path_in)
plot_population(country_boundaries, data, 'GID_1', 'COD')