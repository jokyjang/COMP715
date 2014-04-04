import random
import numpy as np
import time

LAT, LON, TEM = 90, 180, 1800
sst = np.zeros((LAT, LON, TEM), dtype=float)

time1 = time.time()
for lat in range(LAT):
    for lon in range(LON):
        for tem in range(TEM):
            sst[lat, lon, tem] = random.uniform(-50, 50)
time2 = time.time()
print 'simulating costs', time2-time1, 's'

corr = np.zeros((LAT,LON), dtype=float)
time1 = time.time()
lat2 = 45
lon2 = 90
for lat1 in range(LAT):
    for lon1 in range(LON):
        corr[lat1, lon1] = np.corrcoef(sst[lat1,lon1,:], sst[lat2,lon2,:])[0,1]
        #for lat2 in range(lat1+1, LAT):
        #    for lon2 in range(lon1+1, LON):
        #        corr[lat1*lon1, lat2*lon2] = 0
        #        np.corrcoef(sst[lat1,lon1,:], sst[lat2,lon2,:])
time2 = time.time()
print 'calculating corr costs', time2 - time1, 's'

lat1, lon1, lat2, lon2 = 3, 4, 55, 106
print lat1*2-90, lon1*2-180, corr[lat1, lat1]