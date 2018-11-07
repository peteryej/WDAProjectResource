
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
        if (charList[-1] == '1'):
            charList[-1] = '0' 
        elif charList[-1] == '0': 
            charList[-1] = '1' 
        elif charList[-1] == '2': 
            charList[-1] = '3' 
        elif charList[-1] == '3': 
            charList[-1] = '2'
        else:
            print('wrong serial port detected')
            return None 
        targetPort = "".join(charList)
        target = serial.Serial(port=targetPort, timeout=10000, baudrate=9600)
        try:
            discard = target.read(0)
        finally:
            target.close()
        s = serial.Serial(port=serialStr, timeout=10000, baudrate=8000000)
        powerdueThread = PowerDue(s, fName=fName, debug=False)
        powerdueThread.start()
        return powerdueThread


def refreshSerialPorts():
    comportlist = []
    itportList = serial.tools.list_ports.comports()
    for port in itportList:
        comportlist.append(port.device)
        print port.device


if __name__ == "__main__":
    refreshSerialPorts()

    port1 = raw_input("Enter the first port numer (ttyACM...) just a single number: ")
    if (port1):
        file1Default ='test'+ str(port1) + ".csv"
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
            file2Default ='test'+  str(port2) + ".csv"
            file2 = raw_input(
                "Enter the second filename (default: %s): " % file2Default)
            if not file2:
                file2 = file2Default
            # print(file2)
            thread2 = openSerialPort('/dev/ttyACM' + str(port2), file2)
        thread1 = openSerialPort('/dev/ttyACM' + str(port1), file1)
        # print(file1)
        print(datetime.datetime.now())
        if thread2:
            thread2.join()
        if thread1:
            thread1.join()
        print('finished')


    else:
        print('No port entered. Goodbye.')
