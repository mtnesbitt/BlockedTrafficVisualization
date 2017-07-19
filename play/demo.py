from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

fig = plt.figure()
m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=70,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')

m.drawcoastlines()

bethlehem_lat, bethlehem_lon = 40.6552, -75.3814

x,y = m([0, bethlehem_lon], [0, bethlehem_lat])

line = m.drawgreatcircle(0, 0, bethlehem_lon, bethlehem_lat,)[0]

print(line)

def init():
    line.set_data([0, bethlehem_lon], [0, bethlehem_lat])
    return line,


# animation function.  This is called sequentially
def animate(i):
    lons, lats =  np.random.random_integers(-90, 90, 2)
    x, y = m([lons, bethlehem_lon], [lats, bethlehem_lat])

    #m.drawgreatcircle(lons, lats, bethlehem_lon, bethlehem_lat)
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=20, interval=500, blit=False)

plt.show()