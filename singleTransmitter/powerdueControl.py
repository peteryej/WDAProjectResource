
import time
import datetime
import sys
import socket
import serial
import serial.tools.list_ports
from powerdueStream import PowerDue

HOST, PORT = "localhost", 9999

LOG_FILE = '/home/peter/Desktop/competition_results/competitionLogSingle.txt'


def openSerialPort(serialStr):

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
    target = serial.Serial(port=targetPort, timeout=10000, baudrate=115200)
    try:
        discard = target.read(5)
    finally:
        target.close()    



def refreshSerialPorts():
    foundACM0 = False
    itportList = serial.tools.list_ports.comports()
    for port in itportList:
        if (port.device.find('ACM0') > 0):
            foundACM0 = True
        print port.device
    if not (foundACM0):
        print('foundACM0: %s' % foundACM0)
        quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('wrong input format. Like: teamName try1')
        quit()

    refreshSerialPorts()

    energy = [0.0,0.0,0.0]

    # assumes that instrumentation ports are on ..31
    fh = open(LOG_FILE, "a") 
    fh.write('\n---------------new round----------------\n')

    port1 = raw_input("Enter the instrumentation port numer (ttyACM...) just a single number: ") # '1'
    file1 = sys.argv[1] + sys.argv[2] + ".csv"

    print(file1)
    fh.write(file1+'\n')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)

    serialStr = '/dev/ttyACM' + str(port1)
    # start streaming in another thread
    #beforeInstruSerial = time.time()
    s = serial.Serial(port=serialStr, timeout=10000, baudrate=8000000)
    #afterInstruSerial = time.time()
    powerdueThread = PowerDue(s, fName=file1, energy=energy, debug=False)
    #powerdueObject = time.time()
    powerdueThread.start()
    #startedInstru = time.time()

    # open the target port
    openSerialPort(serialStr)
    #openedTarget = time.time()

    
    startTime = datetime.datetime.now()
    # print('open instrumentation time: {}'.format(afterInstruSerial-beforeInstruSerial))
    # print('powerdueObject time: {}'.format(powerdueObject - afterInstruSerial))
    # print('start thread time: {}'.format(startedInstru - afterInstruSerial))
    # print('open target time: {}'.format(openedTarget - startedInstru))

    print('--------start time--------------')
    print(startTime)
    fh.write(startTime.strftime('%Y-%m-%d %H:%M:%S.%f') + '\n\n')

    try:
        # Connect to server and receive data
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

        sock.send('ACK!')
    finally:
        sock.close()

        powerdueThread.join()
        fh.write('processor energy: {0:.5f} \n'.format(energy[0]))
        fh.write('radio energy: {0:.5f} \n'.format(energy[1]))
        fh.write('total energy: {0:.5f} \n'.format(energy[2]))
        fh.close()
        print('finished')



