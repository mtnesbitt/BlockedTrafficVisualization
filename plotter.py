from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import animation
from attack_info_manager import AttackInfoManager

fig = plt.figure(figsize=(12,9))
m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=70,\
            llcrnrlon=-180,urcrnrlon=180)

m.drawcoastlines()

data = AttackInfoManager(25, 100, 10)
xx, yy = m(data.get_lons(), data.get_lats())
scatter = m.scatter(xx, yy, s=data.get_sizes(), c=data.get_colors())


def init():
    return scatter


def animate(i):
    data.update()
    xx, yy = m(data.get_lons(), data.get_lats())
    # values need to be a 2D array, and zip makes a generator of tuples
    scatter.set_offsets([list(a) for a in zip(xx, yy)])
    scatter.set_color(data.get_colors())
    scatter.set_sizes(data.get_sizes())
    return scatter


anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               interval=50, blit=False)

#anim.save('blocked.gif', dpi=80, writer='imagemagick')
plt.show()