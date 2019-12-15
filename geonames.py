# Adapted from https://stackoverflow.com/questions/34498417/import-text-file-from-geonames-using-pandas-python
import pandas as pd
from fuzzywuzzy import process, fuzz
import time

columns = {
    'geonameid': float,
    'name': str,
    'asciiname': str,
    'alternatenames': str,
    'latitude': float,
    'longitude': float,
    'featureclass': str,
    'featurecode': str,
    'countrycode': str,
    'countrycode2': str,
    'admin1code': str,
    'admin2code': str,
    'admin3code': str,
    'admin4code': str,
    'population': float,
    'elevation': float,
    'dem': float,  # dem (digital elevation model)
    'timezone': str,
    'modificationdate': str
}


# Remove readme from zip first
t = time.time()
data = pd.read_csv(
    "data/US.zip", sep="\t", dtype=columns, low_memory=True, names=columns.keys()
)
print(time.time()-t)

t = time.time()

import re

name = 'Fort Worth'
state = 'TX'

d = data[data['name'].str.match(f'^{name}', flags=re.IGNORECASE)]  # feature name
d = d[d['admin1code'].str.match(state, flags=re.IGNORECASE)]  # state

search = process.extractOne(name, d['name'], scorer=fuzz.token_set_ratio)
z = d.loc[search[-1]]
print(float(z['latitude']), float(z['longitude']), fuzz.token_sort_ratio(name, search[0]))  # lat, lon, certainty
