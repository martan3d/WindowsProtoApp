
# PTConfigure Version of Xbee communications  for windows

import serial

## MRBUS Protothrottle utility routines

def mrbusCRC16Calculate(data):
   mrbusPktLen = data[2]
   crc = 0
   for i in range(0, mrbusPktLen):
      if i == 3 or i == 4:
         continue
      else:
         a = data[i]
      crc = mrbusCRC16Update(crc, a)
   return crc

def mrbusCRC16Update(crc, a):
   MRBus_CRC16_HighTable = [ 0x00, 0xA0, 0xE0, 0x40, 0x60, 0xC0, 0x80, 0x20, 0xC0, 0x60, 0x20, 0x80, 0xA0, 0x00, 0x40, 0xE0 ]
   MRBus_CRC16_LowTable =  [ 0x00, 0x01, 0x03, 0x02, 0x07, 0x06, 0x04, 0x05, 0x0E, 0x0F, 0x0D, 0x0C, 0x09, 0x08, 0x0A, 0x0B ]
   crc16_h = (crc>>8) & 0xFF
   crc16_l = crc & 0xFF
   i = 0
   while i < 2:
      if i != 0:
         w = ((crc16_h << 4) & 0xF0) | ((crc16_h >> 4) & 0x0F)
         t = (w ^ a) & 0x0F
      else:
         t = (crc16_h ^ a) & 0xF0
         t = ((t << 4) & 0xF0) | ((t >> 4) & 0x0F)
      crc16_h = (crc16_h << 4) & 0xFF
      crc16_h = crc16_h | (crc16_l >> 4)
      crc16_l = (crc16_l << 4) & 0xFF
      crc16_h = crc16_h ^ MRBus_CRC16_HighTable[t]
      crc16_l = crc16_l ^ MRBus_CRC16_LowTable[t]
      i = i + 1
   return (crc16_h<<8) | crc16_l

##
## Main Xbee Class.  Everything lives here
##
## AT commands to this Xbee
## AT commands REMOTE to other Xbees on the network
## Directed 64 bit address commands to other Xbees on the network
## PAN Broadcast Commands (for PT communications)
##
## get packet - returns list of bytes of raw API message from the above commands
##

class xbeeController:
    def __init__(self):
        # start on COM1, open each until we find the Xbee
        self.sp = None
        for p in range(1, 20):
            port = 'COM{}'.format(p)
            try:
               sp = serial.Serial(port, 38400, timeout=0.25)
               self.sp = sp
               return
            except:
               pass

    def getStatus(self):
        return self.sp

    def close(self):
        self.sp.close()

    def clear(self):
        if self.sp != None:
           self.sp.reset_input_buffer()

    def xbeeReturnResult(self, datalength):
        return(self.sp.read(datalength))

##
## Get Packet - main read of Xbee message coming in from the outside world
## Returns a list containing the actual API message bytea
##

    def getPacket(self):
        r = self.sp.read(1)      ## look for waiting byte in the buffer
        if r == '':
           return None           ## Nothing there, return None
        try:
           d = ord(r)            ## Something there, is it legal?
        except:
           return None           ## No, bad stuff, leave with None

        if d != 0x7e:            ## Made it to here, is it the header of message?
          while(1):              ## It should be otherwise we have a problem
             print("NOT HEADER") ## We should NOT be in the middle of a message, bad
             try:
                d = ord(self.sp.read(1))
             except:
                print ("BAD BYTE")
                return None      ## if bad stuff, just bag it

             if d == None:       ## if nothing, bag it
                print ("NOTHING")
                return None

             if d == 0x7e:       ## otherwise, hae we found beginning of next?
                print ("FOUND START")
                break            ## Means we lost one somewhere

        l1 = self.sp.read(1)     ## length byte SHOULD be the beginning
        if l1 == '':
           print ("ERROR - Low")
           return None           ## Bad if not

        lh = ord(l1)             ## Get low byte of length

        l2 = self.sp.read(1)     ## This should be high byte of length
        if l2 == '':
           print ("ERROR - High")
           return None ## Bad if not there
        ll = ord(l2)

        l = lh << 8
        l = lh | ll

        ## Valid (we hope) length computed, read the rest all at once

        try:
           data = self.sp.read(l+1)
        except:
           return None

        r = []
        r.append(d)
        r.append(lh)
        r.append(ll)

        for p in data:
            r.append(ord(chr(p)))
        return r

##
## Send BroadcastRequest to Xbee for r/w data to/from Protothrottle
## Max length is 12 for all transactions, read and write
## This follows the MRBUS configuration for PT compatibility
##
##  'R', LSB, MSB, LEN - read from PT EE (LSB,MSB), LEN bytes
##  'W', LSB, MSB, DATA, DATA, DATA etc - write data to Protothrottle
##

    def xbeeBroadCastRequest(self, dest, src, data):
        pktLen = 10 + len(data) # MRBus overhead, 5 XBee, and the data
        frame = []
        frame.append(0x7e)	     # 0 - Start
        frame.append(0)              # 1 - Len MSB
        frame.append(pktLen)         # 2 - Len LSB
        frame.append(0x01)           # 3 - COMMAND - transmit 16 bit address
        frame.append(0x00)	     # 4 - frame ID for ack- 0 = disable
        frame.append(0xFF)           # 5 - MSB of dest address - broadcast 0xFFFF
        frame.append(0xFF)	     # 6 - LSB of dest address
        frame.append(0)	             # 7 - Transmit Options

        # mrbus stuff
        frame.append(dest)           # 8 / 0 - Destination
        frame.append(src)            # 9 / 1 - Source
        frame.append(len(data) + 5)  # 10/ 2 - Length
        frame.append(0)              # 11/ 3 - CRC High
        frame.append(0)              # 12/ 4 - CRC Low

        for b in data:
           frame.append(int(b) & 0xFF)

        # this is specific to the mrbus implementation in the PT
        crc = mrbusCRC16Calculate(frame[8:])
        frame[11] = 0xFF & crc
        frame[12] = 0xFF & (crc >> 8)

        xbeeChecksum = 0
        for i in range(3, len(frame)):
           xbeeChecksum = (xbeeChecksum + frame[i]) & 0xFF
        xbeeChecksum = (0xFF - xbeeChecksum) & 0xFF;
        frame.append(xbeeChecksum)

        txBufferEscaped = [ frame[0] ]

        escapedChars = frozenset([0x7E, 0x7D, 0x11, 0x13])

        for i in range(1, len(frame)):
           if frame[i] in escapedChars:
              txBufferEscaped.append(0x7D)
              txBufferEscaped.append(frame[i] ^ 0x20)
           else:
              txBufferEscaped.append(frame[i])

        self.sp.write(txBufferEscaped)


##
## Send AT Command to Xbee
##

    def xbeeDataQuery(self, cmdh, cmdl):
        frame = []
        c0 = ord(cmdl)
        c1 = ord(cmdh)
        frame.append(0x7e)	    # header
        frame.append(0)	            # our data is always fixed size
        frame.append(4)             # this is all data except header, length and checksum
        frame.append(0x08)          # AT COMMAND - send Query to Xbee module
        frame.append(0x52)	    # frame ID for ack- 0 = disable
        frame.append(c1)	    # Command high character
        frame.append(c0)	    # low character
        frame.append(0)	            # zero checksum location

        cks = 0;
        for i in range(3,7):	    # compute checksum
            cks = cks + frame[i]

        i = (255-cks) & 0x00ff
        frame[7] = i	            # and put it in the message

        for i in range(0,8):
            t = chr(frame[i])
            self.sp.write(t.encode())

##
## Send Directed Message to an Xbee on the Network
##

    def xbeeTransmitDataFrame(self, dest, data):
        txdata = []
        dl = len(data)
        for d in data:     # make sure it's in valid bytes for transmit
            try:
               txdata.append(int(ord(d)))
            except:
               txdata.append(int(d))

        frame = []
        frame.append(0x7e)	# header
        frame.append(0)	        # our data is always < 256
        frame.append(dl+11)     # all data except header, length and checksum
        frame.append(0x00)      # TRANSMIT REQUEST 64bit (mac) address - send Query to Xbee module
        frame.append(0x01)      # frame ID for ack- 0 = disable

        frame.append(dest[0])   # 64 bit address (mac)
        frame.append(dest[1])
        frame.append(dest[2])
        frame.append(dest[3])
        frame.append(dest[4])
        frame.append(dest[5])
        frame.append(dest[6])
        frame.append(dest[7])

        frame.append(0x00)      # always reserved

        for i in txdata:        # move data to transmit buffer
            frame.append(i)
        frame.append(0)         # checksum position

        cks = 0;
        for i in range(3, dl+14):	# compute checksum
            cks += int(frame[i])

        i = (255-cks) & 0x00ff
        frame[dl+14] = i        # insert checksum in message

        for d in frame:        # transmit message out to Xbee via USB
            t = bytes([d])
            self.sp.write( t )

        p = "Tx : "            # print what we sent in hex
        for d in frame:
            p = p + "%x " % d
        print (p)


##############################################################################

    def xbeeTransmitRemoteCommand(self, dest, cmda, cmdb, data):
        txdata = []
        data = data[:20].strip()
        for d in data:     # make sure it's in valid bytes for transmit
            txdata.append(int(ord(d)))

        cmda = ord(cmda)
        cmdb = ord(cmdb)

        frame = []
        frame.append(0x7e)      # header

        frame.append(0)         # our data is always fixed size, 20 bytes of payload

        length = 15 + len(data)

        frame.append(length)    # this is all data except header, length and checksum
        frame.append(0x17)      # REMOTE AT COMMAND
        frame.append(0x01)      # frame ID for ack- 0 = disable

        frame.append(dest[0])   # 64 bit address (mac)
        frame.append(dest[1])
        frame.append(dest[2])
        frame.append(dest[3])
        frame.append(dest[4])
        frame.append(dest[5])
        frame.append(dest[6])
        frame.append(dest[7])

        frame.append(0xff)      # always reserved
        frame.append(0xfe)

        frame.append(0x02)      # always apply changes immediate

        frame.append(cmda)      # remote command
        frame.append(cmdb)

        for i in txdata:        # move data to transmit buffer
            frame.append(i)
        frame.append(0)         # checksum position

        cks = 0;
        for i in range(3,length+3):   # compute checksum
           cks += frame[i]

        i = (255-cks) & 0x00ff
        frame[length+3] = i
        for d in frame:
            t = bytes([d])
            self.sp.write( t )

        for d in frame:
            p = "%2x - %s" % (d, chr(d))
            print (p,)
        print
        print ("LENGTH", length)
