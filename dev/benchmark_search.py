import os, sys
sys.path.insert(0, os.path.join(sys.path[0], '..'))

import time
import geonames, zipfile

name = 'Bath(Berkeley Springs)'  # (Berkeley Springs, West Virgina)

zipfile = zipfile.ZipFile('US.zip')
geo = geonames.GeoNames(zipfile.open('US.txt'))

# Without specifying state (searches through whole dataset)
timer = time.time()
location = geo.search(name=name, limit=1)
print(time.time()-timer)

# With state specified (filters by state and searches results)
timer = time.time()
location = geo.search(name=name, admin1code='WV', limit=1)
print(time.time()-timer)
