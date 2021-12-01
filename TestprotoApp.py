import wx
import time
import sqlite3
from xbee import *

TITLE = "Protothrottle Xbee Network"
VERSION = "1.0.0"


########################################################################
class MainWindow(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, size=(900,700))
        self.SetBackgroundColour('#e0e0e0')
        self.NumberXbees = 0
        self.frame = parent

        # setup main Xbee interface class
        self.Xbee = xbeeController()

        # font
        self.font = wx.Font(18, family=wx.FONTFAMILY_DEFAULT, style=0, weight=90, encoding = wx.FONTENCODING_DEFAULT)
        self.smallfont = wx.Font(12, family=wx.FONTFAMILY_DEFAULT, style=0, weight=90, encoding = wx.FONTENCODING_DEFAULT)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer   = wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label=TITLE)
        titleSizer.Add(title, 0, wx.CENTER|wx.ALL, 10)
        title.SetFont(self.font)

        self.scanButton = wx.Button(self, label="Scan")
        self.scanButton.Bind(wx.EVT_BUTTON, self.onAddWidget)
        self.scanButton.SetFont(self.font)
        controlSizer.Add(self.scanButton, 0, wx.CENTER|wx.ALL, 20)

#        self.removeButton = wx.Button(self, label="Remove")
#        self.removeButton.Bind(wx.EVT_BUTTON, self.onRemoveWidget)
#        controlSizer.Add(self.removeButton, 0, wx.CENTER|wx.ALL, 5)

        self.mainSizer.Add(titleSizer, 0, wx.CENTER)
        self.mainSizer.Add(controlSizer, 0, wx.CENTER)
        self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER|wx.ALL, 10)

        self.SetSizer(self.mainSizer)

    #----------------------------------------------------------------------
    def onAddWidget(self, event):
        """"""
        self.NumberXbees += 1
        label = "Button %s\nThis is a new button\nthis is a new line" %  self.NumberXbees
        name = "button%s" % self.NumberXbees
        new_button = wx.Button(self, id=self.NumberXbees, size=(220,120), label=label, name=name)
        new_button.Bind(wx.EVT_BUTTON, self.selectXbee)
        new_button.SetBackgroundColour((255, 230, 200, 255))
        new_button.SetFont(self.smallfont)
        self.widgetSizer.Add(new_button, 0, wx.ALL, 5)
        self.frame.fSizer.Layout()
        self.frame.Fit()

    #----------------------------------------------------------------------
    def onRemoveWidget(self, event):
        if self.widgetSizer.GetChildren():
           sizer_item = self.widgetSizer.GetItem(self.NumberXbees-1)
           widget = sizer_item.GetWindow()
           self.widgetSizer.Hide(widget)
           widget.Destroy()
           self.NumberXbees -= 1
           self.frame.fSizer.Layout()
           self.frame.Fit()

    #---------------------------------------------------------------------
    def selectXbee(self, evt):
        be = evt.GetEventObject()
        print (be.GetId())


########################################################################
class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="ProtoApp")
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        panel = MainWindow(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Layout()
        self.Fit()
        self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
