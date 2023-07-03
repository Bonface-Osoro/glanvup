import configparser
import os
import pandas as pd
from glanvup.coverage import CoverageProcess
pd.options.mode.chained_assignment = None

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')

path = os.path.join(DATA_RAW, 'countries.csv')

coverages = CoverageProcess(path, 'ARG')
cov_country = coverages.process_national_coverage()
cov_region = coverages.process_regional_coverage()