
import time
import datetime
import sys
import serial
import serial.tools.list_ports
from powerdueStream import PowerDue


def openSerialPort(serialStr, fName):

    print serialStr
    if serialStr != "":
        charList = list(serialStr)
        charList[-2] = '1' if charList[-2] == '3' else '3'
        targetPort = "".join(charList)
        target = serial.Serial(port=targetPort, timeout=10000, baudrate=96000)
        s = serial.Serial(port=serialStr, timeout=10000, baudrate=8000000)
        powerdueThread = PowerDue(s, fName=fName, debug=False)
        # powerdueThread.setDaemon(True)
        powerdueThread.start()
        # powerdueThread.join()
        # print('finished')
        return powerdueThread


def refreshSerialPorts():
    comportlist = []
    itportList = serial.tools.list_ports.comports()
    for port in itportList:
        comportlist.append(port.device)
        print port.device


if __name__ == "__main__":
    refreshSerialPorts()
    # openSerialPort('/dev/cu.usbmodem14131', 'b001.csv')   #board 001
    # openSerialPort('/dev/cu.usbmodem14111', 'b011.csv')   #board 011

    port1 = raw_input("Enter the first port numer (14...): ")
    if (port1):
        file1Default = str(port1) + ".csv"
        file1 = raw_input(
            "Enter the first filename (default: %s): " % file1Default)
        if not file1:
            file1 = file1Default

        port2 = raw_input("Enter the second port numer (default: none): ")
        while(port2 == port1):
            print("port2 can't be the same as port1")
            port2 = raw_input("Enter the second port numer (default: none): ")

        thread2 = None

        if (port2):
            file2Default = str(port2) + ".csv"
            file2 = raw_input(
                "Enter the second filename (default: %s): " % file2Default)
            if not file2:
                file2 = file2Default
            # print(file2)
            thread2 = openSerialPort('/dev/cu.usbmodem' + str(port2), file2)
        thread1 = openSerialPort('/dev/cu.usbmodem' + str(port1), file1)
        # print(file1)
        print(datetime.datetime.now())
        if thread2:
            thread2.join()
        thread1.join()
        print('finished')


    else:
        print('No port entered. Goodbye.')
