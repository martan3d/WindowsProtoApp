import wx
import time
import sqlite3
from xbee import *
import wx.lib.scrolledpanel as scrolled
from pthrottle import *
from rx import *
from OPT import *

TITLE = "Protothrottle Xbee Network"
VERSION = "1.0.0"

nodelist = []

nodeDict = {}
nodePhysics = {}
nodeNotches = {}
nodeMasks = {}
lookUp = {}

DISCOVERYRESPONSE = 1
INTERNALRESPONSE  = 2
PTBROADCAST       = 3
DIRECTEDRESPONSE  = 4
ACK               = 5
UNKNOWN           = 6

SETNOTCHMASKS    = 51
GETNOTCHMASKS    = 52
SETNOTCH         = 50
READNOTCHES      = 36
RETURNTYPE       = 37
SETCV            = 16
SETTIMEOUT       = 25
SETOUTPUTSMODE   = 26
READPHYSICS      = 53
SETACCELERATION  = 54
SETDECELERATION  = 55
SETBRAKERATE     = 56
SETBRAKEFUNCTION = 57
FACTORYRESET     = 58


# ---------------------------------------------------
# Utility Methods

def idProto(Xbee):
    start = 16
    laddr = start & 0x00ff
    haddr = (start & 0xff00) >> 8

    Xbee.clear()
    Xbee.xbeeBroadCastRequest(48, 154, [ord('R'), laddr, haddr, 12])
    time.sleep(.10)

    t = 0
    while(1):
       retmsg = Xbee.getPacket()
       if retmsg != None:
          if retmsg[13] == 0x72:
             return True
       t = t + 1
       if t > 4:
          return False

# ---------------------------------------------------
def getEEData(Xbee, start):
    t = 0
    laddr = start & 0x00ff
    haddr = (start & 0xff00) >> 8
    #print (laddr, haddr)

    Xbee.xbeeBroadCastRequest(48, 154, [ord('R'), laddr, haddr, 12])

    while(1):
       retmsg = Xbee.getPacket()
       if retmsg != None:
          if retmsg[13] == 0x72:   # lower case 'r'
             return retmsg

       t = t + 1
       if t > 4:
          break

    return None

# get ascii mac address

def getAddress(data):
    addr = ""
    for i in range(10, 18):
        a = "%02x" % data[i]
        addr = addr + a
    return addr

# get the ASCII name NodeID from the 'ND' response message

def getNodeID(data):
    nodeid = ""
    for i in range(19,37):
        if data[i] == 0:
           return nodeid
        d = chr(data[i])
        if d.isalpha() or d.isdigit():
           nodeid = nodeid + d
        else:
           nodeid = nodeid + ' '
    return nodeid

# build bytes address from string

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


########################################################################
class ProtoDialog(wx.Frame):

    def __init__(self, *args, **kw):
       super(ProtoDialog, self).__init__(*args, **kw)
       self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        st = wx.StaticText(panel, label="THIS IS STATIC", pos=(20,20))
        self.Show(True)

    def setOpenWindows(self, windows):
        self.openWindows = windows

    def onClose(self, evt):
        self.Destroy()

########################################################################
class NodeDialog(wx.Frame):

    def __init__(self, *args, **kw):
       super(NodeDialog, self).__init__(*args, **kw)
       self.initUI()

    def initUI(self):
        self.panel  = wx.Panel(self)
        self.Show(True)

    def setOpenWindows(self, windows):
        self.openWindows = windows

    def onClose(self, evt):
        self.Destroy()


########################################################################
class MainWindow(scrolled.ScrolledPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        scrolled.ScrolledPanel.__init__(self, parent, size=(900,700))
        self.SetBackgroundColour('#e0e0e0')
        self.NumberXbees = 0
        self.frame = parent
        self.ptData = []
        self.rxData = []
        self.OpenWindows = {}

        # setup main Xbee interface class
        self.Xbee = xbeeController()
        if self.Xbee.getStatus() != None:
           self.Xbee.clear()
        else:
           wx.MessageBox("No USB/Xbee Found!", "Error" ,wx.OK | wx.ICON_INFORMATION)

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
        self.scanButton.Bind(wx.EVT_BUTTON, self.scanXbee)
        self.scanButton.SetFont(self.font)
        controlSizer.Add(self.scanButton, 0, wx.CENTER|wx.ALL, 20)

        self.mainSizer.Add(titleSizer, 0, wx.CENTER)
        self.mainSizer.Add(controlSizer, 0, wx.CENTER)
        self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER|wx.ALL, 10)

        self.SetSizer(self.mainSizer)
        self.SetupScrolling()

    #----------------------------------------------------------------------
    def AddWidget(self, name, nodeid):
        """"""
        label = "{}\n{}".format(nodeid, name)
        n = int(name, 16)
        n = n & 0x7fff
        lookUp[n] = name
        new_button = wx.Button(self, id=n, size=(220,60), label=label, name=name)
        new_button.Bind(wx.EVT_BUTTON, self.selectXbee)
        new_button.SetBackgroundColour((200, 200, 200, 255))
        new_button.SetFont(self.smallfont)
        item = self.widgetSizer.Add(new_button, 0, wx.ALL|wx.EXPAND, 5)
        item.SetId(n)
        self.frame.fSizer.Layout()
        self.frame.Fit()

    #----------------------------------------------------------------------
    def RemoveWidget(self, name):
        if self.widgetSizer.GetChildren():
           n = int(name, 16)
           n = n & 0x7fff
           sizer_item = self.widgetSizer.GetItemById(n)
           widget = sizer_item.GetWindow()
           self.widgetSizer.Hide(widget)
           widget.Destroy()
           self.frame.fSizer.Layout()
           self.frame.Fit()

    #---------------------------------------------------------------------
    def getProtothrottleData(self):
        offset = 16
        self.ptData = []
        for i in range(0, 20):
            rmsg = getEEData(self.Xbee, offset)
            if rmsg != None:
               for a in rmsg:
                   self.ptData.append(a)
               offset = offset + 12

    #---------------------------------------------------------------------
    # clicked one of the xbee nodes on the screen, send it a message to see
    # what it is, reciever, OpenPT node or real Protothrottle. Real Protothrottle
    # does not answer this message, the others do
    #

    def selectXbee(self, evt):
        be = evt.GetEventObject()
        n = be.GetId()
        address = lookUp[n]

        messageType = self.getData(address, RETURNTYPE, nodeDict)
        print (messageType)

        if messageType == DIRECTEDRESPONSE:
           msgData = nodeDict[address][1]
           nodeid  = nodeDict[address][0]
           moduleType = chr(msgData[9])                           # extract module type code from message

           if moduleType == 'O':
              nFrame = OpenPTFrame(self, title="Open Protothottle {}".format(address), size=(600,800), data=msgData, xbee=self.Xbee, macaddress=address)
              nFrame.Show(True)
              return

           if moduleType == 'W':                                  # Widget receiver
              self.getData(address, READPHYSICS, nodePhysics)     # get remaining data from receiver
              physicsData = nodePhysics[address][1]

              self.getData(address, READNOTCHES, nodeNotches)
              notchData = nodeNotches[address][1]

              self.getData(address, GETNOTCHMASKS, nodeMasks)
              maskData = nodeMasks[address][1]

              nFrame = ReceiverFrame(self, title="{}".format(nodeid), size=(600,800), data=msgData, pdata=physicsData, ndata=notchData, mdata=nodeMasks, xbee=self.Xbee)
              nFrame.Show(True)
              return

#        else:  # no return, must be real protothrottle
#           nFrame = PthrottleFrame(self, title="Protothottle {}".format(address), size=(600,800), data=None)
#           nFrame.Show(True)

    #---------------------------------------------------------------------
    def processProtothrottle(self):
        print ("process protothrottle")
        self.getProtothrottleData()
        pass

    #---------------------------------------------------------------------
    def processReceiver(self, address):
        print ("process receiver")
        self.getMainData(address)

    #---------------------------------------------------------------------
    def getData(self, address, function, dict):
        data    = '01234567890123456789'      # don't care about what we send
        txaddr  = buildAddress(address)       # send to mac address
        data    = chr(function) + data[1:]    # in this case it's just the query byte
        dlen    = len(data)

        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(txaddr, data)

        time.sleep(0.25)

        while(1):
            nodedata = self.pullPacket()
            msgtype = nodedata[0]

            if msgtype == DIRECTEDRESPONSE:
               nodeid = nodeDict[address][0]
               dict[address] = [nodeid, nodedata[3]]
               break

            if msgtype == None:
               break

        return msgtype

    #---------------------------------------------------------------------
    def scanXbee(self, evt):

        self.Xbee.xbeeDataQuery('N','D')    # network discovery, all Xbees answer this

        time.sleep(0.25)

        while(1):
            nodedata = self.pullPacket()
            msgtype = nodedata[0]

            if msgtype == DISCOVERYRESPONSE:
               nodeDict[nodedata[1]] = [nodedata[2], nodedata[3]]
#               print ('nodedata', nodedata)
#               print ('nodeDict', nodeDict)

            if msgtype == None:
               break

        self.DrawWidgets()

    #---------------------------------------------------------------------
    def DrawWidgets(self):
        # go thru dictionary, delete all widgets that have already been drawn
        for n in nodeDict:
            self.RemoveWidget(n)

        # go back thru list, add all
        for n in nodeDict:
            self.AddWidget(n, nodeDict[n][0])

    #---------------------------------------------------------------------
    def pullPacket(self):
        data = self.Xbee.getPacket()

        if data != None:
           p = "Rx : "
           for d in data:
               p = p + "%x " % d
           print (p)

        msgtype = None
        msb     = None
        lsb     = None

        if data != None:
           msgtype = data[3]
           msb     = data[1]
           lsb     = data[2]

           if msgtype == 129:
              if data[7] == 2:
                 #print ("Protothrottle Broadcast")
                 return [PTBROADCAST, None, None, None]

              if data[7] == 0:
                 # process a return directed message from my receiver
                 nodeid  = getNodeID(data)       # yep, grab some stuff
                 address = getAddress(data)      # Node ID and network address
                 return [DIRECTEDRESPONSE, address, nodeid, data]

           if msgtype == 136:
              #print ("node discovery response")
              if lsb > 5:                        # is this from external nodes?
                 nodeid  = getNodeID(data)       # yep, grab some stuff
                 address = getAddress(data)      # Node ID and network address
                 return [DISCOVERYRESPONSE, address, nodeid, None]
              else:
                 #print ("internal ND response")  # otherwise it's from us, just toss it
                 return [INTERNALRESPONSE, None, None, None]

           if msgtype == 137:                    # Log ACKs from any outgoing messages
              print ("ACK")
              return [ACK, None, None, None]

           return [UNKNOWN, None, None, data]

        return [None, None, None, None]

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
