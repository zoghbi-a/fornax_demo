import astropy
import astropy.coordinates as coord
import astropy.units as u
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time

import warnings
warnings.filterwarnings('ignore')

try:
    import pyvo
except ImportError:
    os.system('pip install pyvo')
    import pyvo

try:
    import s3fs
except ImportError:
    os.system('pip install s3fs')
    

if not os.path.exists('fornax-cloud-access-API'):
    os.system('git clone -b add-cloud-utils https://github.com/zoghbi-a/fornax-cloud-access-API.git')
sys.path.insert(0, f'{os.getcwd()}/fornax-cloud-access-API')


def filter_hst_results(query_result):
    """Some filtering"""
    table_result = query_result.to_table()
    table_result = table_result[(table_result['insname'] == 'WFC3/IR') & 
                                (table_result['productType'] == 'preview') &
                                (table_result['energy_bandpassName'] == 'F128N')]
    table_result.sort('name')
    return table_result

def filter_galex_results(query_result):
    """Some filtering"""
    table_result = query_result.to_table()
    table_result = table_result[(table_result['productType'] == 'PREVIEW') &
                                (np.array(['_M82' in x and 'large' in x for x in table_result['name']]))]
    table_result.sort('name')
    return table_result