
import time
import datetime
import sys
import socket
import serial
import serial.tools.list_ports
from powerdueStream import PowerDue

HOST, PORT = "localhost", 9999

LOG_FILE = '/home/peter/Desktop/competition_results/competitionLogDouble.txt'


def getTargetSerialPort(serialStr):

    charList = list(serialStr)
    if (charList[-1] == '1'):
        charList[-1] = '0' 
    elif charList[-1] == '0': 
        charList[-1] = '1' 
    elif charList[-1] == '2': 
        charList[-1] = '3' 
    elif charList[-1] == '3': 
        charList[-1] = '2'
    elif charList[-1] == '4': 
        charList[-1] = '3'
    else:
        print('wrong serial port detected')

    targetPort = "".join(charList)
    #target = serial.Serial(port=targetPort, timeout=100, baudrate=115200)
    return targetPort



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

    energy1 = [0.0,0.0,0.0]
    energy2 = [0.0,0.0,0.0]

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

    serialStr1 = '/dev/ttyACM' + str(port1)
    serialStr2 = '/dev/ttyACM' + str(port2)

    targetPort1 = getTargetSerialPort(serialStr1)
    targetPort2 = getTargetSerialPort(serialStr2)

    #start = time.time()
    # start streaming in another thread
    s = serial.Serial(port=serialStr1, timeout=10000, baudrate=8000000)
    thread1 = PowerDue(s, fName=file1, energy=energy1, debug=False)
    thread1.start()    
    #openedInstru1 = time.time()

    s = serial.Serial(port=serialStr2, timeout=10000, baudrate=8000000)
    thread2 = PowerDue(s, fName=file2, energy=energy2, debug=False)
    thread2.start()    
    #openedInstru2 = time.time()

    target1 = serial.Serial(port=targetPort1, timeout=100, baudrate=115200)
    target2  = serial.Serial(port=targetPort2, timeout=100, baudrate=115200) 
    #opentargets = time.time()

    try:
        discard = target1.read(5)
        #openedTarget1 = time.time()
        discard = target2.read(5)
        #openedTarget2 = time.time()
        startTime = datetime.datetime.now()
    finally:
        pass

    
    # print('open instru1 time: {}'.format(openedInstru1 - start))
    # print('open instru2 time: {}'.format(openedInstru2 - openedInstru1))
    # print('open target1 time: {}'.format(openedTarget1 - opentargets))    
    # print('open target2 time: {}'.format(openedTarget2 - openedTarget1))   

    print('--------start time--------------')
    print(startTime)
    fh.write(startTime.strftime('%Y-%m-%d %H:%M:%S.%f') + '\n\n')

    try:
        # Connect to server and receive data
        sock.connect((HOST, PORT))
        received1 = sock.recv(512)
        print('--------end time--------------')
        print(received1)

        received2 = sock.recv(512)
        print('--------end time--------------')
        print(received2)

        fh.write(received1+'\n')
        endTimeStr = received1.split('\n')[0]
        endTime = datetime.datetime.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S.%f")
        print('-------total time 1------------')
        totalTime = '{} s'.format((endTime-startTime).total_seconds())
        print(totalTime)
        fh.write(totalTime+'\n\n')

        fh.write(received2+'\n')
        endTimeStr = received2.split('\n')[0]
        endTime = datetime.datetime.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S.%f")
        print('-------total time 2------------')
        totalTime = '{} s'.format((endTime-startTime).total_seconds())
        print(totalTime)
        fh.write(totalTime+'\n')

        sock.send('ACK!')
    finally:
        sock.close()


        thread2.join()
        thread1.join()
        target1.close()    
        target2.close()
        fh.write(file1+' processor energy: {0:.5f} \n'.format(energy1[0]))
        fh.write(file1+' radio energy: {0:.5f} \n'.format(energy1[1]))
        fh.write(file1+' total energy: {0:.5f} \n'.format(energy1[2]))

        fh.write(file2+' processor energy: {0:.5f} \n'.format(energy2[0]))
        fh.write(file2+' radio energy: {0:.5f} \n'.format(energy2[1]))
        fh.write(file2+' total energy: {0:.5f} \n'.format(energy2[2]))
        fh.close()

        print('finished')
