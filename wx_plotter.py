#!/usr/bin/env python
import datetime
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from attack_info_manager import AttackInfoManager
from mpl_toolkits.basemap import Basemap
from wx import *
import wx
class TrafficMap(Frame):
    def __init__(self):
        Frame.__init__(self, None, -1,
                       'Moravian Traffic Project', size=(600, 600), pos=(10,10))

        self.SetBackgroundColour("white")

        panel = Panel(self, size=(1000, 1000), pos=(650, 0))

        text = StaticText(panel, -1, style=ALIGN_RIGHT, pos=(10, 10))

        text.SetLabel("Everyday, thousands of users attempt to get past the Moravian firewall and fail "
                      "to do so."
                          "Interested in the tendencies of where these attacks take place,"
                          "we decided to develop a program that takes the IP address"
                          "of each attempt, converts it to longitude/latitude coordinates and plots it on a basemap. "
                            "The color of the dots corresponds to the type of protocol that is being used. "
                            "Red is for tcp, blue is udp, green is icmp, and cyan is gre")
        text.Wrap(600)
        font = wx.Font('70')
        text.SetFont(font)

        text.SetBackgroundColour("WHITE")

        image_panel = Panel(self, pos=(150, 475), size=(1000, 240))
        image_panel.SetBackgroundColour('white')

        img1 = Image("diagram.png", BITMAP_TYPE_ANY)
        w = img1.GetWidth()
        h = img1.GetHeight()

        img2 = img1.Scale(w / 1.7, h / 2)
        sb2 = StaticBitmap(image_panel, -1, BitmapFromImage(img2), pos=(0, 0))

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = FlexGridSizer(cols=2, hgap=10, vgap=10)
        self.sizer = BoxSizer()
        self.sizer.Add(self.canvas)
        self.sizer.Add(panel)
        self.SetSizer(self.sizer)

        self.Fit()

        self.Maximize()
        self.plot_map()
        self.timer = Timer(self)
        self.Bind(EVT_TIMER, self.callback, self.timer)
        self.timer.Start(milliseconds=50, oneShot=False)

    def plot_map(self):
        self.data = AttackInfoManager(100, 10)
        self.ax = self.figure.add_subplot(111)
        self.m = Basemap(projection='cyl', resolution="c", lat_0=0, lon_0=0, ax=self.ax)
        self.m.drawcoastlines()
        xx, yy = self.m(self.data.get_lons(), self.data.get_lats())
        self.scatter = self.m.scatter(xx, yy, s=self.data.get_sizes(), c=self.data.get_colors())
        self.figure.canvas.draw()

    def callback(self, event):
        if(len(self.data.get_attack_times()) == 0):
            timestamp = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(seconds=2),
                                                   '%Y/%m/%d%H:%M:%S')
        else:
            timestamp = self.data.get_attack_times()[-1]
        self.data.get_attacks_since(timestamp)
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
        frame = TrafficMap()
        frame.Show(True)
        return True
app = App(0)
app.MainLoop()