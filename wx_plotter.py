#!/usr/bin/env python
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from attack_info_manager import AttackInfoManager
import sys


from mpl_toolkits.basemap import Basemap

from wx import *


class Map(Frame):
    def __init__(self):
        Frame.__init__(self, None, -1,
                       'CanvasFrame', size=(600, 600), pos=(10,10))

        self.SetBackgroundColour("Gray")

        panel = Panel(self, size=(1000, 1000), pos=(650, 0))

        text = StaticText(panel, -1, style=ALIGN_LEFT, pos=(10, 10))

        text.SetLabel("Lorem ipsum dolor sit amet,"
                          "consectetur adipiscing elit, "+"\n"
                          "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "+"\n"
                          "Ut enim ad minim veniam, "+"\n"
                          "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat." +"\n"
                          "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur." +"\n"
                          "Excepteur sint occaecat cupidatat non proident," + "\n"
                          "sunt in culpa qui officia deserunt mollit anim id est laborum.")

        text.SetBackgroundColour("WHITE")

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = FlexGridSizer(cols=2, hgap=10, vgap=10)
        self.sizer = BoxSizer()
        self.sizer.Add(self.canvas)
        self.sizer.Add(panel)
        self.SetSizer(self.sizer)

        self.Fit()
        self.plot_map()
        self.Maximize()

        self.timer = Timer(self)
        self.Bind(EVT_TIMER, self.callback, self.timer)
        self.timer.Start(milliseconds=50, oneShot=False)

    def plot_map(self):
        self.data = AttackInfoManager(25, 100, 50)
        self.ax = self.figure.add_subplot(111)
        self.m = Basemap(projection='cyl', resolution="c", lat_0=0, lon_0=0, ax=self.ax)
        self.m.drawcoastlines()
        self.m.drawcountries()
        xx, yy = self.m(self.data.get_lons(), self.data.get_lats())
        self.scatter = self.m.scatter(xx, yy, s=self.data.get_sizes(), c=self.data.get_colors())
        self.figure.canvas.draw()

    def callback(self, event):
        self.data.update()
        xx, yy = self.m(self.data.get_lons(), self.data.get_lats())
        # values need to be a 2D array, and zip makes a generator of tuples
        self.scatter.set_offsets([list(a) for a in zip(xx, yy)])
        self.scatter.set_color(self.data.get_colors())
        self.scatter.set_sizes(self.data.get_sizes())
        self.figure.canvas.draw()

class App(App):
    def OnInit(self):
        'Create the main window and insert the custom frame'
        frame = Map()
        frame.Show(True)
        return True
app = App(0)
app.MainLoop()