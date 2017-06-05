import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

filename = '20170531-inbound-block-ips-protocol.txt'

#lons, lats = data_generator.get_data(100)

m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=70,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
m.drawcoastlines()

#xx, yy = m(lons, lats)
#m.plot(xx, yy, 'ro')

bethlehem_lat, bethlehem_lon = 40.6552, -75.3814
paris_lat, paris_lon = 48.8566, 2.3522
sydney_lat, sydney_lon = -33.8688, 151.2093

lats = [bethlehem_lat, paris_lat, sydney_lat]
lons = [bethlehem_lon, paris_lon, sydney_lon]
sizes = [100, 500, 1000]

xx, yy = m(lons, lats)
m.scatter(xx, yy, s=sizes)

#line = m.drawgreatcircle(0, 0, bethlehem_lon, bethlehem_lat,)[0]

plt.show()
