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
    # print(msb)
    # print(lsb)
    moveTilt = [0x84, 0x01, lsb, msb]
    print(moveTilt)
    s.write(moveTilt)


def getPosition():
    command = [0x90, 0x01]
    s.write(command)
    positionData = s.read(2)
    print positionData


# bearing_map(180)
byte_output(6002)


while running:
    print "\nEnter desired PWM value or 0 to exit"
    inValue = int(raw_input())
    #inValue = inValue * 4
    if inValue == 0:
        running = False
    else:
        byte_output(inValue)
        print (inValue / 4)


'''
while(number < 8000):
    byte_output(number)
    number += 60
    print number
    time.sleep(1)


while(number > 3999):
    byte_output(number)
    number -= 60
    print number
    time.sleep(1)
'''


'''
byte_output(3576)
time.sleep(10)
byte_output(8424)
'''
