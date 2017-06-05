import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap

from play.data_generator import get_data

m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=70,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')

print('data generation... ', end='')
lons, lats = get_data(10)
print('done')

nx = 36  # 10 degree for longitude bin
ny = 18  # 10 degree for latitude bin

# form the bins
lon_bins = np.linspace(-180, 180, nx)
lat_bins = np.linspace(-90, 90, ny)

print('histogram2d... ')
# aggregate the number of earthquakes in each bin, we will only use the density
density, lat_edges, lon_edges = np.histogram2d(lats, lons, [lat_bins, lon_bins])

print('done')

# get the mesh for the lat and lon
lon_bins_2d, lat_bins_2d = np.meshgrid(lon_bins, lat_bins)

# convert the bin mesh to map coordinates:
xs, ys = m(lon_bins_2d, lat_bins_2d)  # will be plotted using pcolormesh

# define custom colormap, white -> red, #E6072A = RGB(0.9,0.03,0.16)
cdict = {'red': ((0.0, 1.0, 1.0),
                 (1.0, 0.9, 1.0)),
         'green': ((0.0, 1.0, 1.0),
                   (1.0, 0.03, 0.0)),
         'blue': ((0.0, 1.0, 1.0),
                  (1.0, 0.16, 0.0))}
custom_map = LinearSegmentedColormap('custom_map', cdict)
plt.register_cmap(cmap=custom_map)

# Here adding one row and column at the end of the matrix, so that
# density has same dimension as xs, ys, otherwise, using shading='gouraud'
# will raise error
density = np.hstack((density, np.zeros((density.shape[0], 1))))
density = np.vstack((density, np.zeros((density.shape[1]))))

# Plot heatmap with the custom color map
plt.pcolormesh(xs, ys, density, cmap="custom_map", shading='gouraud')

# Add color bar and
cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2, pad=0.02)
cbar.set_label('Number of earthquakes', size=18)

# Plot blue scatter plot of epicenters above the heatmap:
x, y = m(lons, lats)
m.plot(x, y, 'o', markersize=5, zorder=6, markerfacecolor='#424FA4', markeredgecolor="none", alpha=0.1)

# make image bigger:
plt.gcf().set_size_inches(12, 12)

plt.show()