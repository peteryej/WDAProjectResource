
import time
import datetime
import sys
import socket
import serial
import serial.tools.list_ports
from powerdueStream import PowerDue

HOST, PORT = "localhost", 9999

LOG_FILE = '/home/peter/Desktop/competition_results/competitionLogDouble.txt'


def openSerialPort(serialStr, fName):

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
        discard = target.read(12)
    finally:
        target.close()
    s = serial.Serial(port=serialStr, timeout=10000, baudrate=8000000)
    powerdueThread = PowerDue(s, fName=fName, debug=False)
    powerdueThread.start()
    return powerdueThread


def refreshSerialPorts():
    foundACM0 = False
    foundACM3 = False
    itportList = serial.tools.list_ports.comports()
    for port in itportList:
        if (port.device.find('ACM0') > 0):
            foundACM0 = True
        elif (port.device.find('ACM3') > 0):
            foundACM3 = True
        print port.device
    if not (foundACM3 and foundACM0):
        print('foundACM0: %s' % foundACM0)
        print('foundACM3: %s' % foundACM3)
        quit()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('wrong input format. Like: team1 team2 try1')
        quit()

    refreshSerialPorts()
    # assumes that instrumentation ports are on ..31
    fh = open(LOG_FILE, "a") 
    fh.write('\n---------------new round----------------\n')

    port1 = raw_input("Enter the first instrumentation port numer (ttyACM...) just a single number: ") # '1'
    file1 = sys.argv[1] + sys.argv[3] + ".csv"

    port2 = raw_input("Enter the second instrumentation port numer (ttyACM...) just a single number: ") #'3'
    file2 = sys.argv[2] + sys.argv[3] + ".csv"

    print(file1)
    fh.write(file1+'\n')
    print(file2)
    fh.write(file2+'\n')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)

    thread1 = openSerialPort('/dev/ttyACM' + str(port1), file1)
    thread2 = openSerialPort('/dev/ttyACM' + str(port2), file2)
    print('--------start time--------------')
    startTime = datetime.datetime.now()
    print(startTime)
    fh.write(startTime.strftime('%Y-%m-%d %H:%M:%S.%f') + '\n\n')

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        received = sock.recv(512)
        print('--------end time--------------')
        print(received)
        fh.write(received+'\n')
        endTimeStr = received.split('\n')[0]
        endTime = datetime.datetime.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S.%f")
        print('-------total time------------')
        totalTime = '{} s'.format((endTime-startTime).total_seconds())
        print(totalTime)
        fh.write(totalTime+'\n\n')

        received = sock.recv(512)
        print('--------end time--------------')
        print(received)
        fh.write(received+'\n')
        endTimeStr = received.split('\n')[0]
        endTime = datetime.datetime.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S.%f")
        print('-------total time------------')
        totalTime = '{} s'.format((endTime-startTime).total_seconds())
        print(totalTime)
        fh.write(totalTime+'\n')

        sock.send('ACK!')
    finally:
        sock.close()


    thread2.join()
    thread1.join()
    print('finished')
