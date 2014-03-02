import serial
import time
import sys
import threading

from controls import CANProcessor

class DaemonThread(threading.Thread):

    def __init__(self, threadName, runnable):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True

        self.name = threadName
        self.runnable = runnable

    def kill(self):
        self.running = False

    def run(self):
        print "Started '%s' thread" % self.name
        while self.running:

            ret = self.runnable.run()
            if not ret:
                self.kill()

            time.sleep(.0001)
        print "Stopped '%s' thread" % self.name

class CANStreamReader(DaemonThread):
    def __init__(self, ser, dataCallback):
        DaemonThread.__init__(self, "CAN Stream Reader", self.read)
        self.name = "CAN Stream Reader"

        self.ser = ser
        self.dataCallback = dataCallback

        self.buffer = ""

    def read(self):
        if len(self.buffer):
            if self.buffer.endswith("BUFFER FULL\r\n\r\n>"):
                print "Buffer full! Aborting."
                return False

        while self.ser.inWaiting() and self.running:
            self.buffer += self.ser.read(self.ser.inWaiting())

        if len(self.buffer):
            if not self.buffer.endswith('\r\n'):
                split = self.buffer.split('\r\n')

                #If last command didn't finish with a newline, keep that in buffer.
                #Since fully-ended commands end with a '' in the split, it's ok to
                #always grab that.
                self.buffer = split[-1]

                entries = len(split)-1
                if entries > 0:
                    self.dataCallback(split[:entries])

        return True

class ObdiiCore:
    def __init__(self):
        self.ser = None
        self.streamReaderThread = None
        self.canThread = None

    def connect(self, dev, baud):
        print "Connecting to", dev, "at", baud
        self.ser = serial.Serial(dev, baud)

    def disconnect(self):
        self.ser.close()
        self.ser = None
        print "Disconnected."

    def sendAsyncCommand(self, command, dataCallback):
        self.ser._write(command + '\r\n')

        self.streamReaderThread = CANStreamReader(self.ser, dataCallback)
        self.streamReaderThread.start()

    #JRTODO: need to validate that it stops sending? or expect buffer full?
    def stopAsync(self):
        print "Sending stop it commands"
        self.sendCommand("\r\n")
        self.streamReaderThread.kill()

        print "Waiting for reader thread to die"
        self.streamReaderThread.join()

#    def waitForAsync(self):
#        print "Waiting for reading thread to finish"
#        self.streamReaderThread.join()

    def sendCommand(self, command):
        print "Sending Command:", command
        self.ser._write(command + '\r\n')
        return self.read()

    def read(self):
        buffer = ''

        while True:
            buffer = buffer + self.ser.read(self.ser.inWaiting())
            if buffer.endswith('\r\n\r\n>'):
                return buffer

#    def clearReadBuffer(self):
#        while self.ser.inWaiting() > 0:
#            self.ser.read(self.ser.inWaiting())


class CANBus(ObdiiCore):

    def __init__(self, dev, baud):
        self.dev = dev
        self.baud = baud

    def ati(self):
        return self.sendCommand(self, 'ati')

    def init(self):
        self.connect(self.dev, self.baud)

#        self.clearReadBuffer()#JRTODO: this isn't working

        print self.sendCommand('atl1') #\r\n line endings
        print self.ati()
        print self.sendCommand('ath1') #headers on
        print self.sendCommand('ats1') #include spaces
        print self.sendCommand('atal') #allow long messages
        print self.sendCommand('atsp6') #set to protocol 6, (CAN 11bit ID, 500kbaud)

    def startMonitor(self, senderIds):
        #Clear filters
        print self.sendCommand('stfcp') #clear pass filters
        print self.sendCommand('stfcb') #clear blocking filters
        print self.sendCommand('stfcfc') #clear flow control filters

        #Add filters
        for id in senderIds:
            print self.sendCommand('stfap %s,fff' % hex(id)[2:])

#        print self.sendCommand('stfap 228,fff') #neutral ind
#        print self.sendCommand('stfap 39e,fff') #random steering while stick info

        self.stm()

    #JRTODO: lock out other functions while monitoring in progress
    def stm(self):
        canProcessor = CANProcessor()
        self.canThread = DaemonThread("CAN Processor", canProcessor)
        self.canThread.start()

        self.sendAsyncCommand("stm", canProcessor.processMessages) #monitor using filters

    def stopMonitor(self):
        self.stopAsync()

    def kill(self):
        self.stopMonitor()

        if self.streamReaderThread:
            self.streamReaderThread.kill()
            self.streamReaderThread.join()

        if self.canThread:
            self.canThread.kill()
            self.canThread.join()

        self.disconnect()

