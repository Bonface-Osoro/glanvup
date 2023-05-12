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