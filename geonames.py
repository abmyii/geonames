#!/usr/bin/env python3
"""
Tested only with dumps from http://download.geonames.org/export/dump/, mostly
US. ZIPs must only contain one file (the main data file) as per current pandas
reader requirements (see https://github.com/pandas-dev/pandas/issues/30262 for
more information).
"""
import pandas as pd
import re

from fuzzywuzzy import process
from fuzzywuzzy.fuzz import token_set_ratio, token_sort_ratio

# Adapted from https://stackoverflow.com/a/34499197
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


class GeoNames:

    def __init__(self, data_csv):
        self.data = pd.read_csv(
            data_csv, sep="\t", dtype=columns, names=columns.keys()
        )

    def search(self, name, converter=None, limit=1, **kwargs):
        """Returns the most likely result as a pandas Series"""
        # Interpret 0 or negative numbers as no limit for results
        if limit <= 0:
            limit = None

        # Make a copy of the dataset to preserve the original
        data = self.data

        # Filter data by string queries
        filters = {'name': name, **kwargs}
        for key, string in filters.items():
            data = data[data[key].str.contains(string, case=False, regex=True)]

        # Extract most likely result(s)
        results = []
        matches = process.extract(
            name, data['name'], limit=limit, scorer=token_set_ratio
        )

        for match in matches:
            result = data.loc[match[-1]]  # filter by result index in dataset
            certainty = token_sort_ratio(name, match[0])

            # Convert result if converter specified
            if converter:
                result = converter(result)

            results.append({'result': result, 'certainty': certainty})

        return results


if __name__ == '__main__':
    import io
    import urllib.request as request
    import zipfile

    # Download and test with smallest dump (YU - Yugoslavia)
    YU = request.urlopen('http://download.geonames.org/export/dump/YU.zip')
    zipfile = zipfile.ZipFile(io.BytesIO(YU.read()))

    geo = GeoNames(zipfile.open('YU.txt'))
    print(geo.search(name='Yugoslavia'))
    print(geo.search(name='Yugoslavia', converter=dict))
