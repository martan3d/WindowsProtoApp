import time
import wx
import wx.xrc

adprot = { 0x30 :'A', 0x31 :'B', 0x32 :'C', 0x33 :'D', 0x34 :'E', 0x35 :'F', 0x36 : 'G', 0x37 : 'H', 0x38 : 'I', 0x39 : 'J',
           0x3a : 'K', 0x3b : 'L', 0x3c : 'M', 0x3d : 'N', 0x3e : 'O', 0x3f : 'P', 0x40 : 'Q', 0x41 : 'R', 0x42 : 'S',
           0x43 : 'T', 0x44 : 'U', 0x45 : 'V', 0x46 : 'W', 0x47 : 'X', 0x48 : 'Y', 0x49 : 'Z' }

protad = { 'A': 0x30, 'B': 0x31, 'C': 0x32, 'D': 0x33, 'E': 0x34, 'F': 0x35, 'G': 0x36, 'H': 0x37, 'I': 0x38,
           'J': 0x39, 'K': 0x3a, 'L': 0x3b, 'M': 0x3c, 'N': 0x3d, 'O': 0x3e, 'P': 0x3f,
           'Q': 0x40, 'R': 0x41, 'S': 0x42, 'T': 0x43, 'U': 0x44, 'V': 0x45, 'W': 0x46, 'X': 0x47, 'Y': 0x48, 'Z': 0x49 }


###########################################################################
## IDs for text controls and buttons

PTIDVALUE       = 1
PTIDBUTTON      = 101
BASEIDVALUE     = 3
BASEIDBUTTON    = 102
LOCOADRVALUE    = 5
LOCOADRBUTTON   = 103
CONSISTDIR      = 7
CONSISTADR      = 8
CONSISTBUTTON   = 104

SERVOZEROREV    = 10
SERVOZEROLO     = 11
SERVOZEROHI     = 12
SERVOZEROBUTTON = 105

SERVOONEREV     = 14
SERVOONEFUNC    = 15
SERVOONELO      = 16
SERVOONEHI      = 17
SERVOONEBUTTON  = 106

SERVOTWOREV     = 19
SERVOTWOFUNC    = 20
SERVOTWOLO      = 21
SERVOTWOHI      = 22
SERVOTWOBUTTON  = 107

OUTPUTXFNCODE   = 24
OUTPUTXSTATE    = 25
OUTPUTYFNCODE   = 26
OUTPUTYSTATE    = 27

OUTPUTXBUTTON   = 108
OUTPUTYBUTTON   = 109

WATCHDOGVALUE   = 30
WATCHDOGBUTTON  = 110

BRAKERATE       = 32
BRAKERATEBUTTON = 111
BRAKEFNCODE     = 34
BRAKEFNBUTTON   = 112
ACCEL           = 36
ACCELBUTTON     = 113
DECEL           = 38
DECELBUTTON     = 114

N1LOW           = 40
N1HIGH          = 41
N1OUT           = 42
N1BUTTON        = 115

N2LOW           = 44
N2HIGH          = 45
N2OUT           = 46
N2BUTTON        = 116

N3LOW           = 48
N3HIGH          = 49
N3OUT           = 50
N3BUTTON        = 117

N4LOW           = 52
N4HIGH          = 53
N4OUT           = 54
N4BUTTON        = 118

N5LOW           = 56
N5HIGH          = 57
N5OUT           = 58
N5BUTTON        = 119

N6LOW           = 60
N6HIGH          = 61
N6OUT           = 62
N6BUTTON        = 120

N7LOW           = 64
N7HIGH          = 65
N7OUT           = 66
N7BUTTON        = 121

N8LOW           = 68
N8HIGH          = 69
N8OUT           = 70
N8BUTTON        = 122

SETNODEID       = 123


# MESSAGE IDS

SETBASEADDRESS  = 38
SETPROTOADDRESS = 39
SETLOCOADDRESS  = 40
SETCONSISTADDRESS    = 45
SETCONSISTDIRECTION  = 46
SETSERVOCONFIG = 47
SETTIMEOUT = 25
SETOUTPUTSMODE = 26

###########################################################################

class ReceiverFrame ( wx.Frame ):

    instance = None
    init = 0

    def buildAddress(self, address):
        dest    = [0,0,0,0,0,0,0,0]
        dest[0] = int(address[:2], 16)           # build mac address from ascii display string
        dest[1] = int(address[2:4], 16)
        dest[2] = int(address[4:6], 16)
        dest[3] = int(address[6:8], 16)
        dest[4] = int(address[8:10], 16)
        dest[5] = int(address[10:12], 16)
        dest[6] = int(address[12:14], 16)
        dest[7] = int(address[14:16], 16)
        return dest

    # set the Xbee node id, receiver does not see this, Xbee just uses it

    def handleNodeId(self):
        nodeid = self.nodeid.GetValue()
        self.Xbee.clear()
        txaddr = self.buildAddress(self.macAddress)
        self.Xbee.xbeeTransmitRemoteCommand(txaddr, 'N', 'I', nodeid)    # set node id
        self.Xbee.xbeeTransmitRemoteCommand(txaddr, 'A', 'C', '')        # apply changes
        self.Xbee.xbeeTransmitRemoteCommand(txaddr, 'W', 'R', '')        # write to eeprom
        time.sleep(0.25)

    # set the protothrottle base address, A-Z

    def handleProtoAddress(self):
        baseaddress = protoad[self.PTID.GetValue()]
        datapayload = chr(SETPROTOADDRESS) + baseaddress + '234567890123456789'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), datapayload)
        time.sleep(0.25)
        self.Xbee.getPacket()


    # set the protothrottle Base ID 0-31

    def handleBaseID(self):
        baseid = self.BaseID.GetValue()
        datapayload = chr(SETBASEADDRESS) + baseid[0] + baseid[1] + '34567890123456789'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), datapayload)
        time.sleep(0.25)
        self.Xbee.getPacket()

    # set the consist mode/direction

    def handleConsistMode(self):
        consistdir = self.consistDirection.GetLabel()
        cd = 0
        if consistdir == 'OFF':
           self.consistDirection.SetLabel('FWD')
           cd = 1

        if consistdir == 'FWD':
           self.consistDirection.SetLabel('REV')
           cd = 2

        if consistdir == 'REV':
           self.consistDirection.SetLabel('OFF')
           cd = 0

        datapayload = chr(SETCONSISTDIRECTION) + chr(cd) + '234567890123456789'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), datapayload)
        time.sleep(0.25)
        self.Xbee.getPacket()

    # set consist address

    def handleConsistAddress(self):
        dccaddr = self.ConsistAddress.GetValue()
        dccaddr = "0000" + dccaddr
        dccaddr = dccaddr[-4:]
        print ('dccaddr', dccaddr)
        datapayload = chr(SETCONSISTADDRESS) + dccaddr[0] + dccaddr[1] + dccaddr[2] + dccaddr[3] + '567890123456789'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), datapayload)
        time.sleep(0.25)
        self.Xbee.getPacket()

    # set the PT loco address the Receiver responds to

    def handleLocoAddress(self):
        dccaddr = self.LocoAddress.GetValue()
        dccaddr = "0000" + dccaddr
        dccaddr = dccaddr[-4:]
        print ('dccaddr', dccaddr)
        datapayload = chr(SETLOCOADDRESS) + dccaddr[0] + dccaddr[1] + dccaddr[2] + dccaddr[3] + '567890123456789'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), datapayload)
        time.sleep(0.25)
        self.Xbee.getPacket()

    # set servo parameters

    def setServo(self, servonum):
        if servonum == 0:
           servorev = self.Servo0Rev.GetValue()
           servohi = self.Servo0High.GetValue()
           servolo = self.Servo0Low.GetValue()
           func = "00"

        if servonum == 1:
           servorev = self.Servo1Rev.GetValue()
           servohi = self.Servo1High.GetValue()
           servolo = self.Servo1Low.GetValue()
           func = self.Servo1FnCode.GetValue()

        if servonum == 2:
           servorev = self.Servo2Rev.GetValue()
           servohi = self.Servo2High.GetValue()
           servolo = self.Servo2Low.GetValue()
           func = self.Servo2FnCode.GetValue()

        shigh = "0000" + servohi
        shigh = shigh[-4:]

        slow  = "0000" + servolo
        slow = slow[-4:]

        if servorev == 'true': sr = '1'
        else: sr = '0'

        adr = "00" + func
        addr = adr[-2:]

        datapayload = chr(SETSERVOCONFIG) + str(servonum) + shigh[0] + shigh[1] + shigh[2] + shigh[3] + slow[0] + slow[1] + slow[2] + slow[3] + sr + addr[0] + addr[1] + '3456789'

        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), datapayload)
        time.sleep(0.25)

    # individual servo handlers call the generic above

    def handleServo0Program(self):
        self.setServo(0)

    def handleServo1Program(self):
        self.setServo(1)

    def handleServo2Program(self):
        self.setServo(2)

    # Configure Output X

    def handleOutputX(self):
        fc = self.OutputXFnCode.GetValue()
        out = self.OutputXState.GetValue()
        payload = chr(SETOUTPUTSMODE) + chr(0) + chr(fc) + chr(out) + '5678901201234567'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), payload)
        time.sleep(0.25)

    # Configure Output Y

    def handleOutputY(self):
        fc = self.OutputYFnCode.GetValue()
        out = self.OutputYState.GetValue()
        payload = chr(SETOUTPUTSMODE) + chr(1) + chr(fc) + chr(out) + '5678901201234567'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), payload)
        time.sleep(0.25)

    # Configure Watchdog

    def handleWatchDog(self):
        seconds = self.WatchDog.GetValue()
        payload = chr(SETTIMEOUT) + chr(wdv) + '345678901201234567'
        self.Xbee.clear()
        self.Xbee.xbeeTransmitDataFrame(self.buildAddress(self.macAddress), payload)
        time.sleep(0.25)


    ###### event handler for everyone in the rx screen class

    def OnButton(self, evt):
        be = evt.GetEventObject()
        id = be.GetId()
        print (id)
        method = self.handlers[id]
        method()


    def __new__( self, *args, **kwargs):
        if self.instance is None:
           self.instance = wx.Frame.__new__(self)
        elif not self.instance:
           self.instance = wx.Frame.__new__(self)
        return self.instance

    def __init__( self, parent, title, size, mac, data, pdata, ndata, mdata, xbee):

        if self.init:
           return
        self.init = 1

        # set handler methods to IDs sent by window buttons

        self.handlers = { PTIDBUTTON      : self.handleProtoAddress,
                          BASEIDBUTTON    : self.handleBaseID,
                          LOCOADRBUTTON   : self.handleLocoAddress,
                          CONSISTDIR      : self.handleConsistMode,
                          CONSISTBUTTON   : self.handleConsistAddress,
                          SERVOZEROBUTTON : self.handleServo0Program,
                          SERVOONEBUTTON  : self.handleServo1Program,
                          SERVOTWOBUTTON  : self.handleServo2Program,
                          SETNODEID       : self.handleNodeId,
                          OUTPUTXBUTTON   : self.handleOutputX,
                          OUTPUTYBUTTON   : self.handleOutputY,
                          WATCHDOGBUTTON  : self.handleWatchDog,
                        }

        wx.Frame.__init__ ( self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=size, style=wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.SetBackgroundColour((166, 166, 166))
        self.dataFrame    = data
        self.physicsFrame = pdata
        self.notchFrame   = ndata
        self.maskFrame    = mdata
        self.macAddress   = mac
        self.Xbee         = xbee

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( 22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        self.m_scrolledWindow1.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.nodeid = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, title, wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER )
        self.nodeid.SetFont( wx.Font( 22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer8.Add( self.nodeid, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )


        self.setid = wx.Button( self.m_scrolledWindow1, SETNODEID, u"Set", wx.DefaultPosition, wx.Size( 30,20 ), 0 )
        bSizer8.Add( self.setid, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.setid.Bind(wx.EVT_BUTTON, self.OnButton)


        self.m_staticText43 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, str(self.macAddress), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText43.Wrap( -1 )
        bSizer8.Add( self.m_staticText43, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        bSizer102 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText122 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"ProtoThrottle ID", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText122.Wrap( -1 )
        self.m_staticText122.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText122.SetMinSize( wx.Size( 150,-1 ) )
        bSizer102.Add( self.m_staticText122, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer102.Add( ( 75, 0), 1, wx.EXPAND, 5 )

        ########################################### PT ID
        adr = adprot[int(self.dataFrame[11])]

        self.PTID = wx.TextCtrl( self.m_scrolledWindow1, PTIDVALUE, adr, wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.PTID.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.PTID.SetMinSize( wx.Size( 60,-1 ) )
        bSizer102.Add( self.PTID, 0, wx.ALL, 5 )

        self.PTIDButton = wx.Button( self.m_scrolledWindow1, PTIDBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PTIDButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.PTIDButton.SetMinSize( wx.Size( 50,30 ) )
        self.PTIDButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer102.Add( self.PTIDButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer102, 1, wx.EXPAND, 5 )
        bSizer1021 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1221 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Base ID", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1221.Wrap( -1 )
        self.m_staticText1221.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1221.SetMinSize( wx.Size( 150,-1 ) )
        bSizer1021.Add( self.m_staticText1221, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer1021.Add( ( 75, 0), 1, wx.EXPAND, 5 )

        ########################################### Base ID
        addrbase = str(self.dataFrame[10])

        self.BaseID = wx.TextCtrl( self.m_scrolledWindow1, BASEIDVALUE, addrbase, wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.BaseID.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.BaseID.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1021.Add( self.BaseID, 0, wx.ALL, 5 )

        self.BaseIDButton = wx.Button( self.m_scrolledWindow1, BASEIDBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.BaseIDButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.BaseIDButton.SetMinSize( wx.Size( 50,30 ) )
        self.BaseIDButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer1021.Add( self.BaseIDButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer1021, 1, wx.EXPAND, 5 )
        bSizer1022 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1222 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Loco Address", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1222.Wrap( -1 )
        self.m_staticText1222.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1222.SetMinSize( wx.Size( 150,-1 ) )
        bSizer1022.Add( self.m_staticText1222, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer1022.Add( ( 75, 0), 1, wx.EXPAND, 5 )

        ########################################## Loco Address
        locoaddr = self.dataFrame[12]
        ch = self.dataFrame[13] << 8
        locoaddr = locoaddr | ch

        self.LocoAddress = wx.TextCtrl( self.m_scrolledWindow1, LOCOADRVALUE, str(locoaddr), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.LocoAddress.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.LocoAddress.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1022.Add( self.LocoAddress, 0, wx.ALL, 5 )

        self.LocoAddressButton = wx.Button( self.m_scrolledWindow1, LOCOADRBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LocoAddressButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.LocoAddressButton.SetMinSize( wx.Size( 50,30 ) )
        self.LocoAddressButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer1022.Add( self.LocoAddressButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer1022, 1, wx.EXPAND, 5 )
        bSizer1013 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1213 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Consist", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1213.Wrap( -1 )
        self.m_staticText1213.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1213.SetMinSize( wx.Size( 100,-1 ) )
        bSizer1013.Add( self.m_staticText1213, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer1013.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        ########################################## Consist Direction
        cdir = self.dataFrame[16]
        print ('cdir', cdir)
        consist = 'OFF'
        if cdir == 1: consist = 'FWD'
        if cdir == 2: consist = 'REV'

        self.consistDirection = wx.Button( self.m_scrolledWindow1, CONSISTDIR, consist, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.consistDirection.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.consistDirection.SetMinSize( wx.Size( 50,30 ) )
        self.consistDirection.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer1013.Add( self.consistDirection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ########################################## Consist Address
        consistaddr = self.dataFrame[14]
        ch = self.dataFrame[15] << 8
        consistaddr = consistaddr | ch

        self.ConsistAddress = wx.TextCtrl( self.m_scrolledWindow1, CONSISTADR, str(consistaddr), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.ConsistAddress.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.ConsistAddress.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1013.Add( self.ConsistAddress, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ########################################## Consist Address Prg Button
        self.ConsistAddressButton = wx.Button( self.m_scrolledWindow1, CONSISTBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ConsistAddressButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.ConsistAddressButton.SetMinSize( wx.Size( 50,30 ) )
        self.ConsistAddressButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer1013.Add( self.ConsistAddressButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer1013, 1, wx.EXPAND, 5 )
        bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer26.SetMinSize( wx.Size( 20,20 ) )
        bSizer26.Add( ( 112, 0), 0, wx.EXPAND, 5 )
        self.m_staticText21 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Rev", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )
        self.m_staticText21.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer26.Add( self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        bSizer26.Add( ( 16, 0), 0, wx.EXPAND, 5 )
        self.m_staticText22 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Fn", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )
        bSizer26.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        bSizer26.Add( ( 22, 0), 0, wx.EXPAND, 5 )
        self.m_staticText23 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"LoLim", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText23.Wrap( -1 )
        self.m_staticText23.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer26.Add( self.m_staticText23, 0, wx.ALL, 5 )
        bSizer26.Add( ( 22, 0), 0, wx.EXPAND, 5 )
        self.m_staticText26 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"HiLim", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText26.Wrap( -1 )
        self.m_staticText26.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer26.Add( self.m_staticText26, 0, wx.ALL, 5 )
        bSizer9.Add( bSizer26, 0, wx.EXPAND, 5 )
        bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText121 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Servo 0", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText121.Wrap( -1 )
        self.m_staticText121.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText121.SetMinSize( wx.Size( 100,-1 ) )
        bSizer101.Add( self.m_staticText121, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        ################################################ Servo 0 reverse checkbox
        svrr = self.dataFrame[32]
        checked = False
        if (int(svrr) & 0x01) == 1:
           checked = True

        self.Servo0Rev = wx.CheckBox( self.m_scrolledWindow1, SERVOZEROREV, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Servo0Rev.SetValue(checked)

        bSizer101.Add( self.Servo0Rev, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        bSizer101.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        ################################################ Servo 0 Low Limit
        svlo0 = self.dataFrame[17]               # 9,10
        ch    = self.dataFrame[18] << 8
        svlo0 = svlo0 | ch

        self.Servo0Low = wx.TextCtrl( self.m_scrolledWindow1, SERVOZEROLO, str(svlo0), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo0Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo0Low.SetMinSize( wx.Size( 60,-1 ) )
        bSizer101.Add( self.Servo0Low, 0, wx.ALL, 5 )

        ################################################ Servo 0 High LImit
        svhi0 = self.dataFrame[19]
        ch    = self.dataFrame[20] << 8          # 11,12
        svhi0 = svhi0 | ch

        self.Servo0High = wx.TextCtrl( self.m_scrolledWindow1, SERVOZEROHI, str(svhi0), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo0High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo0High.SetMinSize( wx.Size( 60,-1 ) )
        bSizer101.Add( self.Servo0High, 0, wx.ALL, 5 )

        ################################################ Servo 0 program button
        self.Servo0Button = wx.Button( self.m_scrolledWindow1, SERVOZEROBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Servo0Button.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo0Button.SetMinSize( wx.Size( 50,30 ) )
        self.Servo0Button.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer101.Add( self.Servo0Button, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer101, 1, wx.EXPAND, 5 )
        bSizer1011 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1211 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Servo 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1211.Wrap( -1 )
        self.m_staticText1211.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1211.SetMinSize( wx.Size( 100,-1 ) )
        bSizer1011.Add( self.m_staticText1211, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        ################################################ Servo 1 reverse
        svrr = self.dataFrame[32]
        checked = False
        if (int(svrr) & 0x02) == 2:
           checked = True

        self.Servo1Rev = wx.CheckBox( self.m_scrolledWindow1, SERVOONEREV, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Servo1Rev.SetValue(checked)

        bSizer1011.Add( self.Servo1Rev, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        bSizer1011.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        ################################################ Servo 1 function code
        sv1func = self.dataFrame[30]

        self.Servo1FnCode = wx.TextCtrl( self.m_scrolledWindow1, SERVOONEFUNC, str(sv1func), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo1FnCode.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo1FnCode.SetMinSize( wx.Size( 40,-1 ) )
        bSizer1011.Add( self.Servo1FnCode, 0, wx.ALL, 5 )
        bSizer1011.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        ################################################ Servo 1 low limit
        svlo1 = self.dataFrame[21]               # 9,10
        ch    = self.dataFrame[22] << 8
        svlo1 = svlo1 | ch

        self.Servo1Low = wx.TextCtrl( self.m_scrolledWindow1, SERVOONELO, str(svlo1), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo1Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo1Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1011.Add( self.Servo1Low, 0, wx.ALL, 5 )

        ################################################ Servo 1 high limit
        svhi1 = self.dataFrame[23]
        ch    = self.dataFrame[24] << 8          # 11,12
        svhi1 = svhi1 | ch

        self.Servo1High = wx.TextCtrl( self.m_scrolledWindow1, SERVOONEHI, str(svhi1), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo1High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo1High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1011.Add( self.Servo1High, 0, wx.ALL, 5 )

        ################################################ Servo 1 program
        self.Servo1Button = wx.Button( self.m_scrolledWindow1, SERVOONEBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Servo1Button.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo1Button.SetMinSize( wx.Size( 50,30 ) )
        self.Servo1Button.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer1011.Add( self.Servo1Button, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer1011, 1, wx.EXPAND, 5 )
        bSizer1012 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1212 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Servo 2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1212.Wrap( -1 )
        self.m_staticText1212.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1212.SetMinSize( wx.Size( 100,-1 ) )
        bSizer1012.Add( self.m_staticText1212, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        ############################################### Servo 2 reverse
        svrr = self.dataFrame[32]
        checked = False
        if (int(svrr) & 0x04) == 4:
           checked = True

        self.Servo2Rev = wx.CheckBox( self.m_scrolledWindow1, SERVOTWOREV, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Servo2Rev.SetValue(checked)

        bSizer1012.Add( self.Servo2Rev, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        bSizer1012.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        ############################################### Servo 2 Function code
        sv2func = self.dataFrame[31]

        self.Servo2FnCode = wx.TextCtrl( self.m_scrolledWindow1, SERVOTWOFUNC, str(sv2func), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo2FnCode.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo2FnCode.SetMinSize( wx.Size( 40,-1 ) )

        bSizer1012.Add( self.Servo2FnCode, 0, wx.ALL, 5 )
        bSizer1012.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        ############################################### Servo 2 low limit
        svlo2 = self.dataFrame[25]               # 9,10
        ch    = self.dataFrame[26] << 8
        svlo2 = svlo2 | ch

        self.Servo2Low = wx.TextCtrl( self.m_scrolledWindow1, SERVOTWOLO, str(svlo2), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo2Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo2Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012.Add( self.Servo2Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ############################################### Servo 2 High Limit
        svhi2 = self.dataFrame[27]
        ch    = self.dataFrame[28] << 8          # 11,12
        svhi2 = svhi2 | ch

        self.Servo2High = wx.TextCtrl( self.m_scrolledWindow1, SERVOTWOHI, str(svhi2), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Servo2High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo2High.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1012.Add( self.Servo2High, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ############################################### Servo 2 program
        self.Servo2Button = wx.Button( self.m_scrolledWindow1, SERVOTWOBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Servo2Button.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Servo2Button.SetMinSize( wx.Size( 50,30 ) )
        self.Servo2Button.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer1012.Add( self.Servo2Button, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer1012, 1, wx.EXPAND, 5 )
        bSizer261 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer261.SetMinSize( wx.Size( 20,20 ) )
        bSizer261.Add( ( 190, 0), 0, wx.EXPAND, 5 )

        self.m_staticText231 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Fn Code", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText231.Wrap( -1 )
        self.m_staticText231.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer261.Add( self.m_staticText231, 0, wx.ALL, 5 )
        bSizer261.Add( ( 22, 0), 0, wx.EXPAND, 5 )
        self.m_staticText261 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"State", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText261.Wrap( -1 )
        self.m_staticText261.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer261.Add( self.m_staticText261, 0, wx.ALL, 5 )
        bSizer9.Add( bSizer261, 0, wx.EXPAND, 5 )
        bSizer10121 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText12121 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Output X", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121.Wrap( -1 )
        self.m_staticText12121.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText12121.SetMinSize( wx.Size( 100,-1 ) )
        bSizer10121.Add( self.m_staticText12121, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer10121.Add( ( 75, 0), 0, wx.EXPAND, 5 )

        ################################################ Output X function code
        outputxfn = self.dataFrame[35] & 0x7f

        self.OutputXFnCode = wx.TextCtrl( self.m_scrolledWindow1, OUTPUTXFNCODE, str(outputxfn), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.OutputXFnCode.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputXFnCode.SetMinSize( wx.Size( 60,-1 ) )
        bSizer10121.Add( self.OutputXFnCode, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################ Output X State
        outputxst = (self.dataFrame[35] & 0x80) >> 7

        self.OutputXState = wx.TextCtrl( self.m_scrolledWindow1, OUTPUTXSTATE, str(outputxst), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.OutputXState.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputXState.SetMinSize( wx.Size( 60,-1 ) )
        bSizer10121.Add( self.OutputXState, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################ Output X Program
        self.OutputXButton = wx.Button( self.m_scrolledWindow1, OUTPUTXBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OutputXButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputXButton.SetMinSize( wx.Size( 50,30 ) )
        self.OutputXButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121.Add( self.OutputXButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer10121, 1, wx.EXPAND, 5 )
        bSizer101211 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText121211 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Output Y", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText121211.Wrap( -1 )
        self.m_staticText121211.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText121211.SetMinSize( wx.Size( 100,-1 ) )
        bSizer101211.Add( self.m_staticText121211, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer101211.Add( ( 75, 0), 0, wx.EXPAND, 5 )

        ################################################ Output Y Function code
        outputyfn = self.dataFrame[36] & 0x7f

        self.OutputYFnCode = wx.TextCtrl( self.m_scrolledWindow1, OUTPUTYFNCODE, str(outputyfn), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.OutputYFnCode.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputYFnCode.SetMinSize( wx.Size( 60,-1 ) )
        bSizer101211.Add( self.OutputYFnCode, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################ Output Y State
        outputyst = (self.dataFrame[36] & 0x80) >> 7

        self.OutputYState = wx.TextCtrl( self.m_scrolledWindow1, OUTPUTYSTATE, str(outputyst), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.OutputYState.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputYState.SetMinSize( wx.Size( 60,-1 ) )
        bSizer101211.Add( self.OutputYState, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################ Output Y Program
        self.OutputYButton = wx.Button( self.m_scrolledWindow1, OUTPUTYBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OutputYButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputYButton.SetMinSize( wx.Size( 50,30 ) )
        self.OutputYButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer101211.Add( self.OutputYButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer101211, 1, wx.EXPAND, 5 )
        bSizer2611 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer2611.SetMinSize( wx.Size( 20,20 ) )
        bSizer2611.Add( ( 256, 0), 0, wx.EXPAND, 5 )
        self.m_staticText2611 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Time Sec", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2611.Wrap( -1 )
        self.m_staticText2611.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer2611.Add( self.m_staticText2611, 0, wx.ALL, 5 )
        bSizer9.Add( bSizer2611, 0, wx.EXPAND, 5 )
        bSizer101212 = wx.BoxSizer( wx.HORIZONTAL )

        ############################################### Watchdog title
        self.m_staticText121212 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"WatchDog", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText121212.Wrap( -1 )
        self.m_staticText121212.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText121212.SetMinSize( wx.Size( 100,-1 ) )
        bSizer101212.Add( self.m_staticText121212, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer101212.Add( ( 145, 0), 0, wx.EXPAND, 5 )

        ############################################### Watchdog Value
        watchvalue = self.dataFrame[34]

        self.WatchDog = wx.TextCtrl( self.m_scrolledWindow1, WATCHDOGVALUE, str(watchvalue), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.WatchDog.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.WatchDog.SetMinSize( wx.Size( 60,-1 ) )
        bSizer101212.Add( self.WatchDog, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ############################################### Watchdog Program
        self.WatchDogButton = wx.Button( self.m_scrolledWindow1, WATCHDOGBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.WatchDogButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.WatchDogButton.SetMinSize( wx.Size( 50,30 ) )
        self.WatchDogButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer101212.Add( self.WatchDogButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer101212, 1, wx.EXPAND, 5 )
        #

        self.m_staticline6 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer9.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
        bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText38 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"ESC Mode", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText38.Wrap( -1 )
        self.m_staticText38.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        bSizer35.Add( self.m_staticText38, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer35.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button25 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Physics", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button25.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        bSizer35.Add( self.m_button25, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer9.Add( bSizer35, 1, wx.EXPAND, 5 )

        #
        self.m_staticline1 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer9.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
        bSizer31 = wx.BoxSizer( wx.VERTICAL )
        self.m_staticText35 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"ESC Physics Setup", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText35.Wrap( -1 )
        self.m_staticText35.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer31.Add( self.m_staticText35, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        bSizer9.Add( bSizer31, 0, wx.EXPAND, 5 )
        bSizer1012121 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1212121 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Brake Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1212121.Wrap( -1 )
        self.m_staticText1212121.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1212121.SetMinSize( wx.Size( 120,-1 ) )
        bSizer1012121.Add( self.m_staticText1212121, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer1012121.Add( ( 124, 0), 0, wx.EXPAND, 5 )

        ################################################# Physics Brake Rate
        br0 = self.physicsFrame[10]
        br1 = self.physicsFrame[11]
        brakerate = (br1<<8) | br0

        self.BrakeRate = wx.TextCtrl( self.m_scrolledWindow1, BRAKERATE, str(brakerate), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.BrakeRate.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.BrakeRate.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1012121.Add( self.BrakeRate, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################# Brake Button
        self.BrakeRateButton = wx.Button( self.m_scrolledWindow1, BRAKERATEBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.BrakeRateButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.BrakeRateButton.SetMinSize( wx.Size( 50,30 ) )
        self.BrakeRateButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer1012121.Add( self.BrakeRateButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer1012121, 1, wx.EXPAND, 5 )
        bSizer10121211 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText12121211 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Brake FnCode", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211.Wrap( -1 )
        self.m_staticText12121211.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText12121211.SetMinSize( wx.Size( 150,-1 ) )
        bSizer10121211.Add( self.m_staticText12121211, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer10121211.Add( ( 94, 0), 0, wx.EXPAND, 5 )

        ################################################# Brake Function Code
        fncode = self.physicsFrame[16]

        self.BrakeFnCode = wx.TextCtrl( self.m_scrolledWindow1, BRAKEFNCODE, str(fncode), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.BrakeFnCode.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.BrakeFnCode.SetMinSize( wx.Size( 60,-1 ) )
        bSizer10121211.Add( self.BrakeFnCode, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################# Brake Function Program
        self.BrakeFnCodeButton = wx.Button( self.m_scrolledWindow1, BRAKEFNBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.BrakeFnCodeButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.BrakeFnCodeButton.SetMinSize( wx.Size( 50,30 ) )
        bSizer10121211.Add( self.BrakeFnCodeButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer10121211, 1, wx.EXPAND, 5 )
        bSizer101212111 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText121212111 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Acceleration", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText121212111.Wrap( -1 )
        self.m_staticText121212111.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText121212111.SetMinSize( wx.Size( 150,-1 ) )
        bSizer101212111.Add( self.m_staticText121212111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer101212111.Add( ( 94, 0), 0, wx.EXPAND, 5 )
        self.BrakeFnCodeButton.Bind(wx.EVT_BUTTON, self.OnButton)

        ################################################# Acceleration Value
        ac0 = self.physicsFrame[12]
        ac1 = self.physicsFrame[13]
        acceleration = (ac1<<8) | ac0

        self.Accleration = wx.TextCtrl( self.m_scrolledWindow1, ACCEL, str(acceleration), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Accleration.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Accleration.SetMinSize( wx.Size( 60,-1 ) )
        bSizer101212111.Add( self.Accleration, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################# Acceleration Program
        self.AccelerationButton = wx.Button( self.m_scrolledWindow1, ACCELBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.AccelerationButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.AccelerationButton.SetMinSize( wx.Size( 50,30 ) )
        self.AccelerationButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer101212111.Add( self.AccelerationButton, 0, wx.ALL, 7 )
        bSizer9.Add( bSizer101212111, 1, wx.EXPAND, 5 )
        bSizer101212112 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText121212112 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Deceleration", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText121212112.Wrap( -1 )
        self.m_staticText121212112.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText121212112.SetMinSize( wx.Size( 150,-1 ) )
        bSizer101212112.Add( self.m_staticText121212112, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer101212112.Add( ( 94, 0), 0, wx.EXPAND, 5 )

        ################################################# Deceleration Value
        dc0 = self.physicsFrame[14]
        dc1 = self.physicsFrame[15]
        deceleration = (dc1<<8) | dc0

        self.Deceleration = wx.TextCtrl( self.m_scrolledWindow1, DECEL, str(deceleration), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Deceleration.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Deceleration.SetMinSize( wx.Size( 60,-1 ) )
        bSizer101212112.Add( self.Deceleration, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        ################################################# Deceleration Button
        self.DecelerationButton = wx.Button( self.m_scrolledWindow1, DECELBUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.DecelerationButton.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.DecelerationButton.SetMinSize( wx.Size( 50,30 ) )
        bSizer101212112.Add( self.DecelerationButton, 0, wx.ALL, 7 )
        self.DecelerationButton.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer9.Add( bSizer101212112, 1, wx.EXPAND, 5 )
        self.m_staticline2 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer9.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
        bSizer311 = wx.BoxSizer( wx.VERTICAL )
        self.m_staticText351 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Consist Notch Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText351.Wrap( -1 )
        self.m_staticText351.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer311.Add( self.m_staticText351, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        bSizer9.Add( bSizer311, 0, wx.EXPAND, 5 )
        bSizer2612 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer2612.SetMinSize( wx.Size( 20,20 ) )
        bSizer2612.Add( ( 128, 0), 0, wx.EXPAND, 5 )
        self.m_staticText2311 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"In Low", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2311.Wrap( -1 )
        self.m_staticText2311.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer2612.Add( self.m_staticText2311, 0, wx.ALL, 5 )
        bSizer2612.Add( ( 22, 0), 0, wx.EXPAND, 5 )
        self.m_staticText2612 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"In High", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2612.Wrap( -1 )
        self.m_staticText2612.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer2612.Add( self.m_staticText2612, 0, wx.ALL, 5 )
        bSizer2612.Add( ( 18, 0), 0, wx.EXPAND, 5 )
        self.m_staticText56 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Output", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText56.Wrap( -1 )
        bSizer2612.Add( self.m_staticText56, 0, wx.ALL, 5 )
        bSizer9.Add( bSizer2612, 0, wx.EXPAND, 5 )
        bSizer1012121121 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1212121121 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1212121121.Wrap( -1 )
        self.m_staticText1212121121.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer1012121121.Add( self.m_staticText1212121121, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer1012121121.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        ################################################ Notch 1 Low
        nl = self.notchFrame[11]
        self.Notch1Low = wx.TextCtrl( self.m_scrolledWindow1, N1LOW, str(nl), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch1Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch1Low.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1012121121.Add( self.Notch1Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizer1012121121.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        ################################################ Notch 1 High
        nh = self.notchFrame[12]
        self.Notch1High = wx.TextCtrl( self.m_scrolledWindow1, N1HIGH, str(nh), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch1High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch1High.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1012121121.Add( self.Notch1High, 0, wx.ALL, 5 )

        ################################################ Notch 1 Out
        no = self.notchFrame[13]
        self.Notch1Out = wx.TextCtrl( self.m_scrolledWindow1, N1OUT, str(no), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch1Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch1Out.SetMinSize( wx.Size( 60,-1 ) )
        bSizer1012121121.Add( self.Notch1Out, 0, wx.ALL, 5 )

        ################################################ Notch 1 Prg Button
        self.notch1Prg = wx.Button( self.m_scrolledWindow1, N1BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notch1Prg.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.notch1Prg.SetMinSize( wx.Size( 50,30 ) )
        bSizer1012121121.Add( self.notch1Prg, 0, wx.ALL, 7 )
        self.notch1Prg.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer9.Add( bSizer1012121121, 1, wx.EXPAND, 5 )

        bSizer10121211211 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText12121211211 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211211.Wrap( -1 )
        self.m_staticText12121211211.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer10121211211.Add( self.m_staticText12121211211, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        bSizer10121211211.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        ################################################ Notch 2 Low
        nl = self.notchFrame[14]
        self.Notch2Low = wx.TextCtrl( self.m_scrolledWindow1, N2LOW, str(nl), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch2Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch2Low.SetMinSize( wx.Size( 60,-1 ) )
        bSizer10121211211.Add( self.Notch2Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizer10121211211.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        nh = self.notchFrame[15]
        self.Notch2High = wx.TextCtrl( self.m_scrolledWindow1, N2HIGH, str(nh), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch2High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch2High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211211.Add( self.Notch2High, 0, wx.ALL, 5 )
        no = self.notchFrame[16]
        self.Notch2Out = wx.TextCtrl( self.m_scrolledWindow1, N2OUT, str(no), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch2Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch2Out.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211211.Add( self.Notch2Out, 0, wx.ALL, 5 )

        self.Notch2Button = wx.Button( self.m_scrolledWindow1, N2BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch2Button.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch2Button.SetMinSize( wx.Size( 50,30 ) )
        self.Notch2Button.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121211211.Add( self.Notch2Button, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer10121211211, 1, wx.EXPAND, 5 )

        bSizer10121211212 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText12121211212 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 3", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211212.Wrap( -1 )

        self.m_staticText12121211212.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10121211212.Add( self.m_staticText12121211212, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer10121211212.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        nl = self.notchFrame[17]
        self.Notch3Low = wx.TextCtrl( self.m_scrolledWindow1, N3LOW, str(nl), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch3Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch3Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211212.Add( self.Notch3Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer10121211212.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        nh = self.notchFrame[18]
        self.Notch3High = wx.TextCtrl( self.m_scrolledWindow1, N3HIGH, str(nh), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch3High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch3High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211212.Add( self.Notch3High, 0, wx.ALL, 5 )

        no = self.notchFrame[19]
        self.Notch3Out = wx.TextCtrl( self.m_scrolledWindow1, N3OUT, str(no), wx.DefaultPosition, wx.DefaultSize, style=wx.TE_RIGHT )
        self.Notch3Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch3Out.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211212.Add( self.Notch3Out, 0, wx.ALL, 5 )

        self.notch3Prg = wx.Button( self.m_scrolledWindow1, N3BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notch3Prg.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.notch3Prg.SetMinSize( wx.Size( 50,30 ) )
        self.notch3Prg.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121211212.Add( self.notch3Prg, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer10121211212, 1, wx.EXPAND, 5 )

        bSizer10121211213 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText12121211213 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 4", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211213.Wrap( -1 )

        self.m_staticText12121211213.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10121211213.Add( self.m_staticText12121211213, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer10121211213.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        self.Notch4Low = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch4Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch4Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211213.Add( self.Notch4Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer10121211213.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        self.Notch4High = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch4High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch4High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211213.Add( self.Notch4High, 0, wx.ALL, 5 )

        self.Notch4Out = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch4Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch4Out.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211213.Add( self.Notch4Out, 0, wx.ALL, 5 )

        self.notch4Prg = wx.Button( self.m_scrolledWindow1, N4BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notch4Prg.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.notch4Prg.SetMinSize( wx.Size( 50,30 ) )
        self.notch4Prg.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121211213.Add( self.notch4Prg, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer10121211213, 1, wx.EXPAND, 5 )

        bSizer10121211214 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText12121211214 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 5", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211214.Wrap( -1 )

        self.m_staticText12121211214.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10121211214.Add( self.m_staticText12121211214, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer10121211214.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        self.Notch5Low = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch5Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch5Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211214.Add( self.Notch5Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer10121211214.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        self.Notch5High = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch5High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch5High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211214.Add( self.Notch5High, 0, wx.ALL, 5 )

        self.Notch5Out = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch5Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch5Out.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211214.Add( self.Notch5Out, 0, wx.ALL, 5 )

        self.notch5Prg = wx.Button( self.m_scrolledWindow1, N5BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notch5Prg.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.notch5Prg.SetMinSize( wx.Size( 50,30 ) )
        self.notch5Prg.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121211214.Add( self.notch5Prg, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer10121211214, 1, wx.EXPAND, 5 )

        bSizer10121211215 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText12121211215 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 6", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211215.Wrap( -1 )

        self.m_staticText12121211215.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10121211215.Add( self.m_staticText12121211215, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer10121211215.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        self.Notch6Low = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch6Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch6Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211215.Add( self.Notch6Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer10121211215.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        self.Notch6High = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch6High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch6High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211215.Add( self.Notch6High, 0, wx.ALL, 5 )

        self.Notch6Out = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch6Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch6Out.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211215.Add( self.Notch6Out, 0, wx.ALL, 5 )

        self.notch6Prg = wx.Button( self.m_scrolledWindow1, N6BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notch6Prg.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.notch6Prg.SetMinSize( wx.Size( 50,30 ) )
        self.notch6Prg.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121211215.Add( self.notch6Prg, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer10121211215, 1, wx.EXPAND, 5 )

        bSizer10121211216 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText12121211216 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 7", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211216.Wrap( -1 )

        self.m_staticText12121211216.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10121211216.Add( self.m_staticText12121211216, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer10121211216.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        self.Notch7Low = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch7Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch7Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211216.Add( self.Notch7Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer10121211216.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        self.Notch7High = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch7High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch7High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211216.Add( self.Notch7High, 0, wx.ALL, 5 )

        self.Notch7Out = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch7Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch7Out.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211216.Add( self.Notch7Out, 0, wx.ALL, 5 )

        self.notch7Prg = wx.Button( self.m_scrolledWindow1, N7BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notch7Prg.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.notch7Prg.SetMinSize( wx.Size( 50,30 ) )
        self.notch7Prg.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121211216.Add( self.notch7Prg, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer10121211216, 1, wx.EXPAND, 5 )

        bSizer10121211217 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText12121211217 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Notch 8", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12121211217.Wrap( -1 )

        self.m_staticText12121211217.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer10121211217.Add( self.m_staticText12121211217, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer10121211217.Add( ( 22, 0), 1, wx.EXPAND, 5 )

        self.Notch8Low = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch8Low.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch8Low.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211217.Add( self.Notch8Low, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer10121211217.Add( ( 0, 0), 0, wx.EXPAND, 5 )

        self.Notch8High = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch8High.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch8High.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211217.Add( self.Notch8High, 0, wx.ALL, 5 )

        self.Notch8Out = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Notch8Out.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.Notch8Out.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10121211217.Add( self.Notch8Out, 0, wx.ALL, 5 )

        self.notch8Prg = wx.Button( self.m_scrolledWindow1, N8BUTTON, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notch8Prg.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.notch8Prg.SetMinSize( wx.Size( 50,30 ) )
        self.notch8Prg.Bind(wx.EVT_BUTTON, self.OnButton)

        bSizer10121211217.Add( self.notch8Prg, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer10121211217, 1, wx.EXPAND, 5 )

        self.m_staticline3 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer9.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText68 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Consist Function Flags", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText68.Wrap( -1 )

        self.m_staticText68.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer9.Add( self.m_staticText68, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer80 = wx.BoxSizer( wx.HORIZONTAL )

        self.F00 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F00.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F00, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.F01 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F01", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F01.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F01, 0, wx.ALL, 5 )

        self.F02 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F02", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F02.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F02, 0, wx.ALL, 5 )

        self.F03 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F03", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F03.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F03, 0, wx.ALL, 5 )

        self.F04 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F04", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F04.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F04, 0, wx.ALL, 5 )

        self.F05 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F05", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F05.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F05, 0, wx.ALL, 5 )

        self.F06 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F06", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F06.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F06, 0, wx.ALL, 5 )

        self.F07 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F07", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F07.SetMinSize( wx.Size( 38,-1 ) )

        bSizer80.Add( self.F07, 0, wx.ALL, 5 )


        bSizer9.Add( bSizer80, 0, wx.EXPAND, 5 )

        bSizer801 = wx.BoxSizer( wx.HORIZONTAL )

        self.F08 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F08", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F08.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F08, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.F09 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F09", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F09.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F09, 0, wx.ALL, 5 )

        self.F10 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F10", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F10.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F10, 0, wx.ALL, 5 )

        self.F11 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F11", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F11.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F11, 0, wx.ALL, 5 )

        self.F12 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F12", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F12.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F12, 0, wx.ALL, 5 )

        self.F13 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F13", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F13.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F13, 0, wx.ALL, 5 )

        self.F14 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F14", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F14.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F14, 0, wx.ALL, 5 )

        self.F15 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"F15", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.F15.SetMinSize( wx.Size( 38,-1 ) )

        bSizer801.Add( self.F15, 0, wx.ALL, 5 )


        bSizer9.Add( bSizer801, 0, wx.EXPAND, 5 )


        self.m_staticline5 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer9.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText48 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Configuration Variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText48.Wrap( -1 )

        self.m_staticText48.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer9.Add( self.m_staticText48, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer2613 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer2613.SetMinSize( wx.Size( 20,20 ) )

        bSizer2613.Add( ( 190, 0), 0, wx.EXPAND, 5 )

        self.m_staticText2312 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Address", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2312.Wrap( -1 )

        self.m_staticText2312.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer2613.Add( self.m_staticText2312, 0, wx.ALL, 5 )


        bSizer2613.Add( ( 22, 0), 0, wx.EXPAND, 5 )

        self.m_staticText2613 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2613.Wrap( -1 )

        self.m_staticText2613.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer2613.Add( self.m_staticText2613, 0, wx.ALL, 5 )


        bSizer9.Add( bSizer2613, 0, wx.EXPAND, 5 )

        bSizer1012111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1212111 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"CV 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1212111.Wrap( -1 )

        self.m_staticText1212111.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1212111.SetMinSize( wx.Size( 100,-1 ) )

        bSizer1012111.Add( self.m_staticText1212111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer1012111.Add( ( 75, 0), 0, wx.EXPAND, 5 )

        self.CV1Addr = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV1Addr.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV1Addr.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012111.Add( self.CV1Addr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.CV1Data = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV1Data.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV1Data.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012111.Add( self.CV1Data, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.OutputYButton1 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OutputYButton1.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputYButton1.SetMinSize( wx.Size( 50,30 ) )

        bSizer1012111.Add( self.OutputYButton1, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer1012111, 1, wx.EXPAND, 5 )

        bSizer1012112 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1212112 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"CV 2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1212112.Wrap( -1 )

        self.m_staticText1212112.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1212112.SetMinSize( wx.Size( 100,-1 ) )

        bSizer1012112.Add( self.m_staticText1212112, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer1012112.Add( ( 75, 0), 0, wx.EXPAND, 5 )

        self.CV2Addr = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV2Addr.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV2Addr.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012112.Add( self.CV2Addr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.CV2Data = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV2Data.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV2Data.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012112.Add( self.CV2Data, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.OutputYButton2 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OutputYButton2.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputYButton2.SetMinSize( wx.Size( 50,30 ) )

        bSizer1012112.Add( self.OutputYButton2, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer1012112, 1, wx.EXPAND, 5 )

        bSizer1012113 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1212113 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"CV 3", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1212113.Wrap( -1 )

        self.m_staticText1212113.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1212113.SetMinSize( wx.Size( 100,-1 ) )

        bSizer1012113.Add( self.m_staticText1212113, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer1012113.Add( ( 75, 0), 0, wx.EXPAND, 5 )

        self.CV3Addr = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV3Addr.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV3Addr.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012113.Add( self.CV3Addr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.CV3Data = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV3Data.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV3Data.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012113.Add( self.CV3Data, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.OutputYButton3 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OutputYButton3.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputYButton3.SetMinSize( wx.Size( 50,30 ) )

        bSizer1012113.Add( self.OutputYButton3, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer1012113, 1, wx.EXPAND, 5 )

        bSizer1012114 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1212114 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"CV 4", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1212114.Wrap( -1 )

        self.m_staticText1212114.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1212114.SetMinSize( wx.Size( 100,-1 ) )

        bSizer1012114.Add( self.m_staticText1212114, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer1012114.Add( ( 75, 0), 0, wx.EXPAND, 5 )

        self.CV4Addr = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV4Addr.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV4Addr.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012114.Add( self.CV4Addr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.CV4Data = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CV4Data.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.CV4Data.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1012114.Add( self.CV4Data, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.OutputYButton4 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Prg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.OutputYButton4.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.OutputYButton4.SetMinSize( wx.Size( 50,30 ) )

        bSizer1012114.Add( self.OutputYButton4, 0, wx.ALL, 7 )


        bSizer9.Add( bSizer1012114, 1, wx.EXPAND, 5 )

        self.m_staticline51 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer9.Add( self.m_staticline51, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText40 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Factory Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText40.Wrap( -1 )

        bSizer9.Add( self.m_staticText40, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer37 = wx.BoxSizer( wx.VERTICAL )

        bSizer37.SetMinSize( wx.Size( -1,10 ) )
        self.FactoryReset = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer37.Add( self.FactoryReset, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer9.Add( bSizer37, 0, wx.EXPAND, 5 )
        bSizer8.Add( bSizer9, 0, wx.ALIGN_CENTER_HORIZONTAL, 0 )

        self.m_scrolledWindow1.SetSizer( bSizer8 )
        self.m_scrolledWindow1.Layout()
        bSizer8.Fit( self.m_scrolledWindow1 )
        bSizer3.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer3 )
        self.Layout()

        self.Centre( wx.BOTH )


    def __del__( self ):
        pass




