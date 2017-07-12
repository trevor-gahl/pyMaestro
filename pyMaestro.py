import serial
import time


number = 4000
test_out = [None] * 2
running = True

s = serial.Serial('COM14', 9600, timeout=0.5)


def setTargetMiniSSC(value):
    moveTilt = [0xFF, 0x01, value]
    print(moveTilt)
    s.write(moveTilt)


def setTargetCompact(value):
    msb = (value >> 7) & 0x7F
    lsb = value & 0x7F
    moveTilt = [0x84, 0x01, lsb, msb]
    print(moveTilt)
    s.write(moveTilt)


def getPosition():
    command = [0x90, 0x01]
    s.write(command)
    positionData = s.read(2)
    print positionData


while running:
    print "\nEnter desired PWM value or 0 to exit"
    inValue = int(raw_input())
    if inValue == 0:
        running = False
    else:
        setTargetCompact(inValue)
        print (inValue / 4)
