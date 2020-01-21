geonames
========

Library to query places from GeoName dumps (http://download.geonames.org/export/dump/).

Installation
------------

geonames requires Python 2.7 or 3.5+ as well as ``numpy`` and ``pandas`` packages. It can be installed with,

.. code::

    pip install geonames

Usage
------------
The best way to search for a specific location is to have a "filter" value and then the place's name. The filter will reduce the number of rows to check considerably. For example, when searching for a location in the US there are (currently) 2237584 entries. However, once a state is specified (e.g. West Virigina) the number drops down to 35932; 1/60th of the original number of rows.

.. code-block:: python

    import geonames
    import io
    import urllib.request as request
    import zipfile

    name = 'Bath(Berkeley Springs)'  # (Berkeley Springs, West Virgina)

    # Download US geonames dataset
    US = request.urlopen('http://download.geonames.org/export/dump/US.zip')
    zipfile = zipfile.ZipFile(io.BytesIO(US.read()))

    # Load data
    geo = geonames.GeoNames(zipfile.open('US.txt'))

    # Search with state specified (`admin1code` filters by state)
    location = geo.search(name=name, admin1code='WV', limit=1)[0]
    print(location)

Which (if all goes well) should output:

.. code-block::

    geonameid                                              4.7987e+06
    name                                             Berkeley Springs
    asciiname                                        Berkeley Springs
    alternatenames      Berkeley Spring,Berkeley Springs,Warm Springs
    latitude                                                  39.6264
    longitude                                                -78.2292
    featureclass                                                    H
    featurecode                                                  SPNG
    countrycode                                                    US
    countrycode2                                                  NaN
    admin1code                                                     WV
    admin2code                                                    065
    admin3code                                                    NaN
    admin4code                                                    NaN
    population                                                      0
    elevation                                                     185
    dem                                                           194
    timezone                                         America/New_York
    modificationdate                                       2011-12-12
    certainty                                                      86
    Name: 741633, dtype: object
