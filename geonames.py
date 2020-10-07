#!/usr/bin/env python3
"""
Tested only with dumps from http://download.geonames.org/export/dump/, mostly
US. ZIPs must only contain one file (the main data file) as per current pandas
reader requirements (see https://github.com/pandas-dev/pandas/issues/30262 for
more information).
"""
import difflib
import pandas as pd

# https://stackoverflow.com/a/20627316
pd.options.mode.chained_assignment = None  # default='warn'

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
            data_csv, sep="\t", dtype=columns, names=tuple(columns)
        )

    def search(self, name, converter=None, regex=False, **kwargs):
        """Returns the most likely result as a pandas Series"""
        # Make a copy of the dataset to preserve the original
        data = self.data

        # Filter data by string queries before searching
        filters = {**kwargs}
        for key, val in filters.items():
            data = data[
                data[key].str.contains(val, case=False, regex=regex, na=False)
            ]

        # Use difflib to find matches
        diffs = difflib.get_close_matches(name, data['name'].tolist(), n=1, cutoff=0)
        matches = data[data['name'] == diffs[0]]

        for index, result in matches.iterrows():
            certainty = difflib.SequenceMatcher(None, result['name'], name).ratio()

            # Convert result if converter specified
            if converter:
                result = converter(result)

            result['certainty'] = certainty
            yield result


if __name__ == '__main__':
    import io
    import urllib.request as request
    import zipfile

    # Download and test with smallest dump (YU - Yugoslavia)
    YU = request.urlopen('http://download.geonames.org/export/dump/YU.zip')
    zipfile = zipfile.ZipFile(io.BytesIO(YU.read()))

    geo = GeoNames(zipfile.open('YU.txt'))
    print(next(geo.search(name='Yugoslavia')))
    print(next(geo.search(name='Yugoslavia', converter=dict)))
