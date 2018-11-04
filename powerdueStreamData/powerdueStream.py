#import pyqtgraph as pg
import time, threading, sys
import serial
from time import sleep
import numpy as np
from Queue import Queue
from struct import *

NCHAN = 4
PACKET_SIZE = 1020 #bytes
HDR_SIZE = 8 #bytes, not including sync bytes
NSAMP_PER_PACKET = 16
DATA_SIZE = 2

# 4 bytes of sync
# Task ID 2 bytes
# Timestamp 4 bytes
# packet length 2 bytes
# Actual data

SYNC_BYTE = chr(0x55)
SYNC_BLOCK = 'UUUU'
SYNC_BLOCK_LENGTH = 4

STATE_SYNC = 0
STATE_READING = 1

FILE_PATH = '/home/wdauser/Desktop/testOutput/'

class PowerDue(threading.Thread):
    """ Defines a thread for reading and buffering serial data.
    By default, about 5MSamples are stored in the buffer.
    Data can be retrieved from the buffer by calling get(N)"""
    def __init__(self, port, fName='test.csv', chunkSize=63, chunks=10000, debug = False):
        threading.Thread.__init__(self)
        # circular buffer for storing serial data until it is
        # fetched by the GUI

        self.bufferSize = chunks*chunkSize # Size of the buffer. Used as a utility

        # Buffer holds 4 channels + task ids.
        self.buffer = np.zeros((NCHAN + 1,self.bufferSize), dtype=np.uint16)

        self.chunks = chunks        # number of chunks to store in the buffer
        self.chunkSize = chunkSize  # size of a single chunk (items, not bytes)

        self.ptr = 0                # pointer to most (recently collected buffer index) + 1
        self.port = port            # serial port handle
        self.sps = 0.0              # holds the average sample acquisition rate
        self.exitFlag = False
        self.exitMutex = threading.Lock()
        self.dataMutex = threading.Lock()
        self.testCounter = 0
        # Queue to store commands. pulled in the run method
        self.commandQueue = Queue()

        # if dbug is on, use fake data
        self.debug = debug
        self.duration = 0
        self.fName = fName

    def startCommand(self):
        print "Starting..."
        #self.commandQueue.put('g')
        # Here, we send a serial command to the PowerDue to start.

    def stopCommand(self):
        print "Stopping..."
        #self.commandQueue.put('s')
        # Here, we send a serial command to the PowerDue to stop.

    def run(self):
        """ Main execution thread. Contiuously reads value from serial and puts
        it into a buffer."""

        exitMutex = self.exitMutex
        dataMutex = self.dataMutex
        buffer = self.buffer
        port = self.port
        count = 0
        sps = None
        #lastUpdate = pg.ptime.time()
        tmpData = np.zeros((NCHAN + 1, self.chunkSize), dtype = np.uint16)
        print tmpData.shape
        #self.startCommand()
        start = time.time()
        prev = start

        while True:
            # Check if there is anything in the command queue.
            if not self.commandQueue.empty():
                command = self.commandQueue.get()
                print command
                self.port.write(command)
                self.commandQueue.task_done()
            # see whether an exit was requested
            with exitMutex:
                if self.exitFlag:
                    break

            # Fake data for debug
            if self.debug:
                readData = self.ptr*np.linspace(0, 1, self.chunkSize*NCHAN)*4096/(self.chunkSize*self.chunks)
                task_id = self.ptr % 4
                num_samples = 126
                sleep(0.000254)
            else:
                # Read full packet
                serdata = port.read(PACKET_SIZE)

                # Synchronize with packets coming from PowerDue
                if serdata[0:SYNC_BLOCK_LENGTH] != SYNC_BLOCK:
                    print serdata[0:SYNC_BLOCK_LENGTH]
                    self.synchronize()
                    serdata = port.read(PACKET_SIZE - SYNC_BLOCK_LENGTH)
                else:
                    # Remove sync bytes
                    serdata = serdata[SYNC_BLOCK_LENGTH:]

                # Grab header
                metadata = serdata[0:HDR_SIZE]

                # Unpack the metadata into Task ID (2 Bytes), Timestamp (4 Bytes), Packet Length (2 Bytes)
                md_tuples = unpack('<HIH', metadata)
                #print md_tuples

                # Get the data for each of the parts of the header
                task_id = md_tuples[0]
                timestamp = md_tuples[1]
                packet_length = md_tuples[2]

                packet_length = packet_length - packet_length%8

                # Only recognize the packet_length number of values
                actualdata = serdata[HDR_SIZE:packet_length+HDR_SIZE]

                # Compute the number of samples in packet_length
                #num_samples = packet_length /4/2 if packet_length < PACKET_SIZE-HDR_SIZE else 126
                num_samples =  63

                # convert data to 16bit int numpy array
                readData = np.fromstring(actualdata, dtype=np.uint16)


            for _chan in range(0, NCHAN):
                # Subsample. Start:stop:step
                tmpData[_chan, 0:num_samples] = ((readData[_chan:readData.size:8]).copy() & 0x0FFF)



            # write the new chunk into the circular buffer
            # and update the buffer pointer
            with dataMutex:
                # Check for the end of a buffer. If it's the end, loop back.
                if self.ptr + num_samples >= self.bufferSize:
                    break
                    # Leftover samples
                    delta = self.ptr + num_samples - self.bufferSize
                    buffer[:,self.ptr:self.bufferSize] = tmpData[:,0:num_samples - delta]
                    buffer[:,0:delta] = tmpData[:,num_samples-delta: num_samples]
                else:
                    buffer[:,self.ptr:self.ptr+num_samples] = tmpData[:,0:num_samples]
                self.ptr = (self.ptr + num_samples) % buffer.shape[1]
                #print(self.ptr)

            if time.time() - prev > 1:
                prev = time.time()
                count += 1
                print(str(count) + ' s')

        end = time.time()
        port.close()

        header = 'time (s), ch0 Radios(V), ch1 Actuators(V), ch2 Sensors(V), ch3 Processor(V)'
        #buffer = np.transpose(buffer)
        tVals, dataVals = self.downSampleAndOutput()
        output = np.vstack([tVals, dataVals])
        output = np.transpose(output)
        np.savetxt(FILE_PATH+self.fName, output, fmt="%10.6f", delimiter=",", header = header, comments = '')
        self.duration = end - start
        print('duration: ' + str(self.duration))
        print('data saved as '+FILE_PATH+self.fName)
        self.calcEnergy(output)
        self.exit()


    def downSampleAndOutput(self, downsample=20):
        num = self.buffer.shape[1]
        # print(num)
        vals = self.buffer[0:NCHAN,:].astype(np.float32) * (3.3 / 2**12)

        if downsample > 1:  # if downsampling is requested, average N samples together
            ds_data= vals.reshape((NCHAN,num/downsample,downsample)).mean(axis=2)
            num_ds = ds_data.shape[1]
            return np.linspace(0, (num_ds-1)*4e-5*downsample, num_ds), ds_data
        else:
            return np.linspace(0, (num_ds-1)*4e-5, num), vals


    def calcEnergy(self, output):
        totalRaw = np.sum(output, axis=0)    

        delta = output[-1][0]/output.shape[0]
        ProcessorCol = output[:,4]
        RadioCol = output[:,3]
        ProcessorTotal = np.sum(ProcessorCol[np.where(ProcessorCol>.1)])
        RadioTotal = np.sum(RadioCol)


        Processorenergy = ProcessorTotal*3.3/25/1.33*delta   
        print(self.fName+" Processor energy: {0:.5f} J".format(Processorenergy))
        Radioenergy = RadioTotal*3.3/25/.4*delta   
        print(self.fName+" Radio energy: {0:.5f} J".format(Radioenergy))
        print(self.fName+" Total energy: {0:.5f} J".format(Radioenergy+Processorenergy))
        

    def synchronize(self):
        """ Synchronize serial reads with the packts. Looks for SYNC_BYTE repeated
        four times as the packet header.
        """
        synced = False
        num_count = 0
        while not synced:
            syncb = self.port.read(1)
            if syncb == SYNC_BYTE:
                num_count = num_count + 1
            else:
                num_count = 0
            if num_count == 4:
                synced = True
        print "synced"

    def exit(self):
        """ Instruct the serial thread to exit."""
        self.stopCommand()
        with self.exitMutex:
            self.exitFlag = True


