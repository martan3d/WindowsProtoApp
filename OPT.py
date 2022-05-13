# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
###########################################################################

import wx
import wx.xrc
import time

LOCOADR = 2000
RADIOB0 = 2010
RADIOB1 = 2011
RADIOB2 = 2012
RADIOB3 = 2013
RADIOB4 = 2014

BUTTONRED    = 3100
BUTTONBLUE   = 3101
BUTTONYELLOW = 3102
SWITCH1      = 3103
SWITCH2      = 3104
SWITCH3      = 3105
SWITCH4      = 3106


PROGBUTTON   = 3000

RETURNTYPE = 37
PUTALL     = 0x20


FUNCTIONCHOICES = ['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','F16','F17','F18','F19','F20','F21','F22','F23','F24','F25','F26','F27','F28']

def buildAddress(address):
    dest    = [0,0,0,0,0,0,0,0]
    dest[0] = int(address[:2], 16)           # very brute force way to pull this out!
    dest[1] = int(address[2:4], 16)
    dest[2] = int(address[4:6], 16)
    dest[3] = int(address[6:8], 16)
    dest[4] = int(address[8:10], 16)
    dest[5] = int(address[10:12], 16)
    dest[6] = int(address[12:14], 16)
    dest[7] = int(address[14:16], 16)
    return dest

###########################################################################

class OpenPTFrame ( wx.Frame ):

    instance = None
    init = 0

    def __new__( self, *args, **kwargs):
        if self.instance is None:
           self.instance = wx.Frame.__new__(self)
        elif not self.instance:
           self.instance = wx.Frame.__new__(self)
        return self.instance

#########################################################################################

    def buildData(self):
        data = " "
        for d in range(0, 5):
            data = data + chr((self.locoData[d][0] & 0x00ff))
            data = data + chr((self.locoData[d][0] & 0xff00) >> 8)
            data = data + chr(self.locoData[d][1])
            data = data + chr(self.locoData[d][2])
            data = data + chr(self.locoData[d][3])
            data = data + chr(self.locoData[d][4])
            data = data + chr(self.locoData[d][5])
            data = data + chr(self.locoData[d][6])
            data = data + chr(self.locoData[d][7])

        return data

#
# if any dropdown changes
#

    def controlChanged(self, event):
        be = event.GetEventObject()
        id = be.GetId()

        if id == BUTTONRED:
           selected = self.m_choice1.GetSelection()
           self.locoData[self.locoIndex][1] = selected

        if id == BUTTONBLUE:
           selected = self.m_choice2.GetSelection()
           self.locoData[self.locoIndex][2] = selected

        if id == BUTTONYELLOW:
           selected = self.m_choice3.GetSelection()
           self.locoData[self.locoIndex][3] = selected

        if id == SWITCH1:
           selected = self.m_choice4.GetSelection()
           self.locoData[self.locoIndex][4] = selected

        if id == SWITCH2:
           selected = self.m_choice5.GetSelection()
           self.locoData[self.locoIndex][5] = selected

        if id == SWITCH3:
           selected = self.m_choice6.GetSelection()
           self.locoData[self.locoIndex][6] = selected

        if id == SWITCH4:
           selected = self.m_choice7.GetSelection()
           self.locoData[self.locoIndex][7] = selected

#
# program button
#

    def buttonClicked(self, event):
        be = event.GetEventObject()
        n = be.GetId()

        function = PUTALL
        data = self.buildData()
        txaddr = buildAddress(self.macaddr)  # send to mac address
        data   = chr(function) + data[1:]

        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(txaddr, data)

        time.sleep(0.25)

#
# Loco Address
#

    def setLocoAddress(self, event):      # on text entry
        be = event.GetEventObject()
        id = be.GetId()
        if id == 2000:
           try:
              self.locoData[self.locoIndex][0] = int(self.m_textCtrl2.GetValue())
           except:
              self.locoData[self.locoIndex][0] = 0

#
# Radio button, loco select
#

    def onRadioGroup(self, event):       # on click
        be = event.GetEventObject()
        n = be.GetId()

        self.locoIndex = n - RADIOB0
        displayAddress = str(self.locoData[self.locoIndex][0])    ###
        self.m_textCtrl2.SetValue(displayAddress)

        self.m_choice1.SetSelection( self.locoData[self.locoIndex][1] )
        self.m_choice2.SetSelection( self.locoData[self.locoIndex][2] )
        self.m_choice3.SetSelection( self.locoData[self.locoIndex][3] )
        self.m_choice4.SetSelection( self.locoData[self.locoIndex][4] )
        self.m_choice5.SetSelection( self.locoData[self.locoIndex][5] )
        self.m_choice6.SetSelection( self.locoData[self.locoIndex][6] )
        self.m_choice7.SetSelection( self.locoData[self.locoIndex][7] )


#############################################################################################

    def __init__( self, parent, title, size, data, xbee, macaddress ):

        if self.init:
           return
        self.init = 1

        self.Xbee = xbee
        self.macaddr = macaddress
        self.locoData = []
        self.locoIndex = 0

        for d in range(10, len(data)-9, 9):
            locoadr = data[d+1]
            locoadr = locoadr << 8
            locoadr |= data[d] & 0x00ff
            self.locoData.append( [locoadr, data[d+2], data[d+3], data[d+4], data[d+5], data[d+6], data[d+7], data[d+8]])

        wx.Frame.__init__ ( self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=size, style=wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        pageSizer = wx.BoxSizer( wx.VERTICAL )

        TitleAndMacSizer = wx.BoxSizer( wx.VERTICAL )
        TitleAndMacSizer.Add( ( 0, 20), 0, 0, 5 )

        self.OpenPT = wx.StaticText( self, wx.ID_ANY, u"OpenPT", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OpenPT.Wrap( -1 )
        self.OpenPT.SetFont( wx.Font( 22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        TitleAndMacSizer.Add( self.OpenPT, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.macAddr = wx.StaticText( self, wx.ID_ANY, macaddress, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.macAddr.Wrap( -1 )
        TitleAndMacSizer.Add( self.macAddr, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        pageSizer.Add( TitleAndMacSizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

        pageSizer.Add( ( 0, 20), 0, wx.EXPAND, 5 )

        locoAddress = wx.BoxSizer( wx.VERTICAL )

        displayAddress = str(self.locoData[self.locoIndex][0])    ###

        self.m_textCtrl2 = wx.TextCtrl( self, LOCOADR, displayAddress, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl2.SetFont( wx.Font( 28, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_textCtrl2.Bind(wx.EVT_TEXT, self.setLocoAddress)

        locoAddress.Add( self.m_textCtrl2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        pageSizer.Add( locoAddress, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
        pageSizer.Add( ( 0, 20), 0, 0, 5 )

        locoButtons = wx.BoxSizer( wx.HORIZONTAL )

        self.m_radioLoco1 = wx.RadioButton( self, RADIOB0, u"Loco 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioLoco1.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_radioLoco1.SetValue(1)
        self.m_radioLoco1.Bind(wx.EVT_RADIOBUTTON, self.onRadioGroup)

        locoButtons.Add( self.m_radioLoco1, 0, wx.ALL, 5 )

        self.m_radioLoco2 = wx.RadioButton( self, RADIOB1, u"Loco 2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioLoco2.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_radioLoco2.Bind(wx.EVT_RADIOBUTTON, self.onRadioGroup)

        locoButtons.Add( self.m_radioLoco2, 0, wx.ALL, 5 )

        self.m_radioLoco3 = wx.RadioButton( self, RADIOB2, u"Loco 3", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioLoco3.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_radioLoco3.Bind(wx.EVT_RADIOBUTTON, self.onRadioGroup)

        locoButtons.Add( self.m_radioLoco3, 0, wx.ALL, 5 )

        self.m_radioLoco4 = wx.RadioButton( self, RADIOB3, u"Loco 4", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioLoco4.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_radioLoco4.Bind(wx.EVT_RADIOBUTTON, self.onRadioGroup)

        locoButtons.Add( self.m_radioLoco4, 0, wx.ALL, 5 )

        self.m_radioLoco5 = wx.RadioButton( self, RADIOB4, u"Loco 5", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_radioLoco5.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_radioLoco5.Bind(wx.EVT_RADIOBUTTON, self.onRadioGroup)

        locoButtons.Add( self.m_radioLoco5, 0, wx.ALL, 5 )
        pageSizer.Add( locoButtons, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
        pageSizer.Add( ( 0, 20), 0, 0, 5 )

        topButtons = wx.BoxSizer( wx.HORIZONTAL )

        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        self.m_bpButton1 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
        self.m_bpButton1.SetBitmap( wx.Bitmap( u"images/rb.png", wx.BITMAP_TYPE_ANY ) )
        bSizer7.Add( self.m_bpButton1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        m_choice1Choices = FUNCTIONCHOICES
        self.m_choice1 = wx.Choice( self, BUTTONRED, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        self.m_choice1.SetSelection( self.locoData[self.locoIndex][1] )
        self.m_choice1.Bind(wx.EVT_CHOICE, self.controlChanged)
        bSizer7.Add( self.m_choice1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        topButtons.Add( bSizer7, 1, 0, 5 )

        topButtons.Add( ( 30, 0), 0, 0, 5 )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.m_bpButton2 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.m_bpButton2.SetBitmap( wx.Bitmap( u"images/bb.png", wx.BITMAP_TYPE_ANY ) )
        bSizer8.Add( self.m_bpButton2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        m_choice2Choices = FUNCTIONCHOICES
        self.m_choice2 = wx.Choice( self, BUTTONBLUE, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
        self.m_choice2.SetSelection( self.locoData[self.locoIndex][2] )
        self.m_choice2.Bind(wx.EVT_CHOICE, self.controlChanged)
        bSizer8.Add( self.m_choice2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        topButtons.Add( bSizer8, 1, 0, 5 )
        topButtons.Add( ( 30, 0), 0, 0, 5 )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_bpButton3 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.m_bpButton3.SetBitmap( wx.Bitmap( u"images/yb.png", wx.BITMAP_TYPE_ANY ) )
        bSizer9.Add( self.m_bpButton3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        m_choice3Choices = FUNCTIONCHOICES
        self.m_choice3 = wx.Choice( self, BUTTONYELLOW, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
        self.m_choice3.SetSelection( self.locoData[self.locoIndex][3] )
        self.m_choice3.Bind(wx.EVT_CHOICE, self.controlChanged)
        bSizer9.Add( self.m_choice3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        topButtons.Add( bSizer9, 1, 0, 5 )


        pageSizer.Add( topButtons, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        pageSizer.Add( ( 0, 60), 0, 0, 5 )

        bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        self.m_bpButton4 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.m_bpButton4.SetBitmap( wx.Bitmap( u"images/switch.png", wx.BITMAP_TYPE_ANY ) )
        bSizer18.Add( self.m_bpButton4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        m_choice4Choices = FUNCTIONCHOICES
        self.m_choice4 = wx.Choice( self, SWITCH1, wx.DefaultPosition, wx.DefaultSize, m_choice4Choices, 0 )
        self.m_choice4.SetSelection( self.locoData[self.locoIndex][4] )
        self.m_choice4.Bind(wx.EVT_CHOICE, self.controlChanged)
        bSizer18.Add( self.m_choice4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        bSizer17.Add( bSizer18, 1, 0, 5 )

        bSizer19 = wx.BoxSizer( wx.VERTICAL )

        self.m_bpButton5 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.m_bpButton5.SetBitmap( wx.Bitmap( u"images/switch.png", wx.BITMAP_TYPE_ANY ) )
        bSizer19.Add( self.m_bpButton5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        m_choice5Choices = FUNCTIONCHOICES
        self.m_choice5 = wx.Choice( self, SWITCH2, wx.DefaultPosition, wx.DefaultSize, m_choice5Choices, 0 )
        self.m_choice5.SetSelection( self.locoData[self.locoIndex][5] )
        self.m_choice5.Bind(wx.EVT_CHOICE, self.controlChanged)
        bSizer19.Add( self.m_choice5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        bSizer17.Add( bSizer19, 1, 0, 5 )

        bSizer20 = wx.BoxSizer( wx.VERTICAL )

        self.m_bpButton6 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.m_bpButton6.SetBitmap( wx.Bitmap( u"images/switch.png", wx.BITMAP_TYPE_ANY ) )
        bSizer20.Add( self.m_bpButton6, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        m_choice6Choices = FUNCTIONCHOICES
        self.m_choice6 = wx.Choice( self, SWITCH3, wx.DefaultPosition, wx.DefaultSize, m_choice6Choices, 0 )
        self.m_choice6.SetSelection( self.locoData[self.locoIndex][6] )
        self.m_choice6.Bind(wx.EVT_CHOICE, self.controlChanged)
        bSizer20.Add( self.m_choice6, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        bSizer17.Add( bSizer20, 1, 0, 5 )

        bSizer21 = wx.BoxSizer( wx.VERTICAL )

        self.m_bpButton7 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.m_bpButton7.SetBitmap( wx.Bitmap( u"images/switch.png", wx.BITMAP_TYPE_ANY ) )
        bSizer21.Add( self.m_bpButton7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        m_choice7Choices = FUNCTIONCHOICES
        self.m_choice7 = wx.Choice( self, SWITCH4, wx.DefaultPosition, wx.DefaultSize, m_choice7Choices, 0 )
        self.m_choice7.SetSelection( self.locoData[self.locoIndex][7] )
        self.m_choice7.Bind(wx.EVT_CHOICE, self.controlChanged)
        bSizer21.Add( self.m_choice7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        bSizer17.Add( bSizer21, 1, 0, 5 )

        pageSizer.Add( bSizer17, 1, wx.EXPAND, 5 )

        pageSizer.Add( ( 0, 20), 0, 0, 5 )
        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_button1 = wx.Button( self, PROGBUTTON, u"Program", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button1.SetFont( wx.Font( 24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_button1.Bind(wx.EVT_BUTTON,self.buttonClicked)
        bSizer14.Add( self.m_button1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        pageSizer.Add( bSizer14, 1, wx.EXPAND, 5 )

        self.SetSizer( pageSizer )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass





