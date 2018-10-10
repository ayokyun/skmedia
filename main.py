import serial
from devices.inverters import esp3k5


print(esp3k5)


esp = esp3k5.Esp3k5(1)


with serial.Serial('COM8', 9600, timeout=0.2) as ser:
    print(esp.makeQuery())
    ser.write(esp.makeQuery())
    line = ser.readline()  # read a '\n' terminated line

    print(line)
