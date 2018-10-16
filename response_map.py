# TODO
# import lang_dist from metadata and identify lat-long

# fix Basemap installation
"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
"""



#map = Basemap(projection='merc', lat_0 = 57, lon_0 = -135,
#    resolution = 'h', area_thresh = 0.1,
#    llcrnrlon=-136.25, llcrnrlat=56.0,
#    urcrnrlon=-134.25, urcrnrlat=57.75)
"""
fig = plt.figure(figsize=(6,6), dpi = 300)
ax = fig.add_axes([0.1,0.1,0.8,0.8])
lons = [-3.44,9.5,5.29,10.45,14.5,2.21,8.47]
lats = [55.38,56.26,52.13,51.17,58.13,46.23,60.47]
map = Basemap(projection='merc',
    resolution = 'l', area_thresh = 0.1,
    llcrnrlon=-10, llcrnrlat=45,
    urcrnrlon=22.4, urcrnrlat=61)
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'white')
map.drawmapboundary()

x,y = map(lons, lats)
for i in range(len(x)):
    #size = (np.log(lang_dist[i])+1)*15
    size = 7 * (np.log(lang_dist[i])+1)
    #map.plot(x[i], y[i], 'o', color = '0.25', markeredgecolor = 'k', markersize = size, alpha = 0.5)
    map.plot(x[i], y[i], 'o', color = 'r', markeredgecolor = None, markersize = size, alpha = 0.5)
plt.savefig('lang2map.png')
plt.close()
"""
