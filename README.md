# WindowsProtoApp

WX Python OpenPTC, Receiver and Protothrottle Windows Programmer UI

This program is designed to be an alternative to my raspberry pi based stand alone programmer.  

I have tested this with Windows 7, 10 and 11. It's pretty basic, it should work with most Windows versions.

The interface is a USB cable with an Xbee 'dongle' on the end. Plug that into your Windows PC and run this python program.

The Xbee must be an S2C or better and be running the 802.15.4 TH firmware. Use the Digi XCTU utility to verify this. Zigbee or Digimesh will not work.

The dongle must have the correct USB drivers installed.  I use the WaveShare device available on Amazon, it uses the Silicon Labs USB Driver.

If you look at the code it assumes the USB port to the Xbee is simple serial port

----------------------------------------------------------------------------------

With XCTU, insure the Xbee is set to a PAN ID of 225, this is where the Protothrottle Lives.

Set the 16bit source address to 3039. The Receiver needs to see a directed message from this address.

Also set the API mode to 1 - (API Mode without Escapes [1])

The UART baud rate needs to be 38400, No Parity, One stop bit.

----------------------------------------------------------------------------------

There is python code in the xbee module that supports the R/W of the Protothrottle EEPROM

It is not implemented in the WX UI but has been tested with the latest Protothrottle Firmware.  

Feel free to experiment.




