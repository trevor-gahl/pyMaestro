import serial
import time


class Maestro:

    #s = serial.Serial('COM14', 9600, timeout=0.5)

    def __init__(self):
        comPort = searchComPorts()
        self.usb = serial.Serial(comPort, 9600)
        self.running = True

    def close(self):
        self.usb.close()

    def searchComPorts():
        ports = list(serial.tools.list_ports.comports())
        try:		# Mini Maestro shows up as Pololu Micro Maestro 6, but with 2 ports. We want the command port
            if eachLst[1].find("Pololu Micro Maestro 6") and eachLst[2].find("Servo Controller Command Port") != -1:
                servoCOM = eachLst[0].strip()
                return servoCOM

        except:		# Because not every port has 2 '-' characters, the split function may not work
            if (each.vid == 8187 and each.pid == 137) and each.location is None:
                servoCOM = eachLst[0].strip()
                return servoCOM

    def setTargetMiniSSC(self, channel, value):
        command = [0xFF, channel, value]
        print(moveTilt)
        self.usb.write(moveTilt)

    def setTargetCompact(self, channel, value):
        msb = (value >> 7) & 0x7F
        lsb = value & 0x7F
        command = [0x84, channel, lsb, msb]
        print(moveTilt)
        self.usb.write(moveTilt)

    def getPosition(self, channel):
        command = [0x90, channel]
        self.usb.write(command)
        positionData = self.usb.read(2)
        lsb = ord(positionData[0])
        msb = ord(positionData[1])
        value = (msb << 8) | lsb
        print value

    def setSpeed(self, channel, value):
        msb = (value >> 7) & 0x7F
        lsb = value & 0x7F
        command = [0x87, channel, lsb, msb]
        self.usb.write(command)

    def setAcceleration(self, channel, value):
        msb = (value >> 7) & 0x7F
        lsb = value & 0x7F
        command = [0x89, channel, lsb, msb]
        self.usb.write(command)

    def getErrors(self):
        command = [0xA1]
        self.usb.write(command)
        errorData = int(self.usb.read(1))
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

    def initTest(self):
        setSpeed(1, 1)
        setAcceleration(1, 1)
        setTargetCompact(6000)
        getPosition()
        getErrors()
        setTargetCompact(5000)
        setTargetCompact(6000)


while running:
    print "\nEnter desired PWM value or 0 to exit"
    inValue = int(raw_input())
    if inValue == 0:
        running = False
    else:
        setTargetCompact(inValue)
        print (inValue / 4)
        getPosition()
