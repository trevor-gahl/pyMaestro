#########################################################################################
## Name: Trevor Gahl                                                                   ##
## Date: 7/12/2017                                                                     ##
## Desc: Program communicates with the Pololu Maestro servo controller to drive servos ##
#########################################################################################

import serial
import serial.tools.list_ports


class Maestro:

    def __init__(self):
        comPort = self.searchComPorts()
        print comPort
        self.usb = serial.Serial(comPort, 9600)

    def close(self):
        self.usb.close()

    ##########################################
    ## Autodetect COM Port for Mini-Maestro ##
    ##########################################
    def searchComPorts(self):
        ports = list(serial.tools.list_ports.comports())
        for each in ports:
            print(each)
            eachLst = str(each).split('-')
            try:		# Mini Maestro shows up as Pololu Micro Maestro 6, but with 2 ports. We want the command port
                if eachLst[1].find("Pololu Micro Maestro 6") and eachLst[2].find("Servo Controller Command Port") != -1:
                    servoCOM = eachLst[0].strip()
                    print servoCOM
                    return servoCOM

            except:		# Because not every port has 2 '-' characters, the split function may not work
                if (each.vid == 8187 and each.pid == 137) and each.location is None:
                    servoCOM = eachLst[0].strip()
                    print servoCOM
                    return servoCOM

    ################################################
    ## Move to target position (8-bit resolution) ##
    ################################################
    def setTargetMiniSSC(self, channel, value):
        command = [0xFF, channel, value]
        print(command)
        self.usb.write(command)

    #################################################
    ## Move to target position (14-bit resolution) ##
    #################################################
    def setTargetCompact(self, channel, value):
        msb = (value >> 7) & 0x7F
        lsb = value & 0x7F
        command = [0x84, channel, lsb, msb]
        print(command)
        self.usb.write(command)

    #########################################
    ## Reads in last sent positional value ##
    #########################################
    def getPosition(self, channel):
        command = [0x90, channel]
        self.usb.write(command)
        positionData = self.usb.read(2)
        lsb = ord(positionData[0])
        msb = ord(positionData[1])
        value = (msb << 8) | lsb
        print value

    ############################
    ## Sets servo speed value ##
    ############################
    def setSpeed(self, channel, value):
        msb = (value >> 7) & 0x7F
        lsb = value & 0x7F
        command = [0x87, channel, lsb, msb]
        self.usb.write(command)

    ###################################
    ## Sets servo acceleration value ##
    ###################################
    def setAcceleration(self, channel, value):
        msb = (value >> 7) & 0x7F
        lsb = value & 0x7F
        command = [0x89, channel, lsb, msb]
        self.usb.write(command)

    ###########################################
    ## Reads in any error codes from Maestro ##
    ###########################################
    def getErrors(self):
        command = [0xA1]
        self.usb.write(command)
        errorData = ord(self.usb.read(1))
        if errorData == 1:
            print "Serial signal error"
        elif errorData == 2:
            print "Serial overrun error"
        elif errorData == 4:
            print "Serial buffer full"
        elif errorData == 8:
            print "Serial CRC error"
        elif errorData == 16:
            print "Serial protocol error"
        elif errorData == 32:
            print "Serial timeout"
        elif errorData == 64:
            print "Script stack error"
        elif errorData == 128:
            print "Script call stack error"
        else:
            print "No errors"

    ####################################
    ## Method to test library methods ##
    ####################################
    def initTest(self):
        self.setSpeed(1, 1)
        self.setAcceleration(1, 1)
        self.setTargetCompact(1, 6000)
        self.getPosition(1)
        self.getErrors()
        self.setTargetCompact(1, 5000)
        self.setTargetCompact(1, 6000)


###################################################################
## Example usage of library with a simple command line interface ##
###################################################################
running = True
maestro = Maestro()
maestro.initTest()

while running:
    print "\nEnter desired PWM value or 0 to exit"
    inValue = int(raw_input())
    if inValue == 0:
        running = False
    else:
        maestro.setTargetCompact(1, inValue)
        print (inValue / 4)
        maestro.getPosition(1)
