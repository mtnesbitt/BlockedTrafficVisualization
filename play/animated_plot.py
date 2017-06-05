
import requests
import json
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


filename = '20170531-inbound-block-ips-protocol.txt'

locations = {}

m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=70,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')

m.drawcoastlines()
m.drawcountries()
m.drawstates()

count = 0

with open(filename, 'r') as f:
    for line in f:
        (date, time, ip, protocol) = line.split()

        if ip not in locations:
            r = requests.get('http://localhost:8080/json/' + ip)
            info = json.loads(r.text)
            locations[ip] = (float(info['latitude']), float(info['longitude']), info['country_name'])

            lat = float(info['latitude'])
            lon = float(info['longitude'])
            name = info['country_name']
        else:
            (lat, lon, name) = locations[ip]

        x, y = m(lon, lat)

        m.plot(x, y, 'ro')  # plot a blue dot there
        # put some text next to the dot, offset a little bit
        # (the offset is in map projection coordinates)
        #plt.text(x + 100000, y + 100000, name)

        #m.scatter(lat, lon, latlon=True, linewidths=100)

        print(ip, lat, lon, x, y, name)

        count += 1
        if count == 1000:
            break

lon, lat = -104.237, 40.125
x, y = m(lat, lon)
m.plot(x, y, 'ro')

plt.show()