import serial
import time


number = 4000
test_out = [None] * 2
running = True

#s = serial.Serial('COM4', 9600, timeout=0.5)


def bearing_map(bearing):
    output = bearing - (180 - (180 - 12)) * (1212) / (180 + (180 - 12)
                                                      ) - (180 - (180 - 12)) + 894 + (1212 * (894 / 360))
    panTo = ((bearing - (155 - 168)) * (2106 - 894) /
             ((155 + 168) - (155 - 168)) + 894) + (1212 * 894 / 360)

    bearing = (bearing - 180)
    if bearing < 0:
        bearing = bearing + 360
    bearing = int((bearing * 3.37 + 893.4) * 4)
    print output
    print panTo
    print bearing


def byte_output(value):
    msb = (value >> 7) & 0x7F
    lsb = value & 0x7F
    # print(msb)
    # print(lsb)
    moveTilt = [0x84, 0x00, lsb, msb]
    # print(moveTilt)
    # s.write(moveTilt)


# bearing_map(180)
while running:
    print "\nEnter desired PWM value or 0 to exit"
    inValue = int(raw_input("Input PWM Value: "))
    if inValue == 0:
        running = False
    byte_output(5500)


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
