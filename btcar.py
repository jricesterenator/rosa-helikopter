import serial
import time
import sys
import threading
from serial.tools import list_ports

serialClass = serial.Serial

ser = None

class ReadingThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = True

        self.f = open('/tmp/log.txt', 'w')

    def run(self):
        print "Starting " + self.name
        self.read()
        self.f.flush()
        self.f.close()
        print "Exiting " + self.name

    def kill(self):
        self.running = False

    def read(self):
        lastread = time.time()
        lastwritten = ""
        buffer = ""
        notifiedNoData = False
        while time.time() - lastread < 3 and self.running: #no data in last 5 seconds
            timediff = time.time() - lastread
            if timediff > .5 and self.running:
                if not notifiedNoData:
                    notifiedNoData=True
                    print "No data", timediff
                    print "LAST RECEIVED WAS", [lastwritten]
                    print "LAST IN BUFFER", [buffer[:50]]
                if len(buffer):
                    if buffer.endswith("BUFFER FULL\r\n\r\n>"):
                        print "Buffer was full, sending newline to get more data."
                        ser._write('\r\n')
                        lastread = time.time()
                        notifiedNoData=False
                elif lastwritten.endswith("BUFFER FULL\r\n\r\n>"):
                    print "Buffer was full, sending newline to get more data."
                    ser._write('\r\n')
                    lastread = time.time()
                    notifiedNoData=False

            time.sleep(.01)

            while ser.inWaiting() and self.running:
                buffer += ser.read(ser.inWaiting())
                lastread = time.time()
            if len(buffer) >= 5000:
#                print "WRITING TO FILE"
                lastwritten = buffer[-50:]
                self.f.write(buffer)
                self.f.flush()
                buffer = ""

            time.sleep(.0001)

        print "WRITING FINAL DATA"
        if len(buffer):
            self.f.write(buffer)
            self.f.flush()


def connect(dev, baud):
    print "Connecting to", dev, "at", baud
    global ser
    ser = serialClass(dev, baud)

def disconnect():
    global ser
    ser.close()
    ser = None

    print "Disconnected."


##JRTODO what's the proper way to kill this command. keep sending \r\n and it keeps giving more
global rt
rt = None
def stopAsync():
    global rt
    rt.kill()
    print "Sending stop it commands"
    sendCommand("\r\n")

    print "Waiting for reader thread to die"
    rt.join()


def sendAsyncCommand(command):
    ser._write(command + '\r\n')

    global rt
    rt = ReadingThread(1, 'reading thread')
    rt.start()

def b2b():
    sendAsyncCommand('atma')
    time.sleep(.1)
    ser._write('\r\n')

def waitForAsync():
    print "Waiting for reading thread to finish"
    global rt
    rt.join()

def sendCommand(command):
    ser._write(command + '\r\n')
    return read()

def read():
    buffer = ''

    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if buffer.endswith('\r\n\r\n>'):
            return buffer


def listSerialPorts():
    ports = [p[0] for p in list_ports.comports()]

    print "Available serial ports:"
    for p in ports:
        print "  " + p


#########
# Convenience functions
#########

def ati():
    return sendCommand('ati')

#sets the protocol to automatic
def atsp0():
    return sendCommand('atsp0')

def atma():
    sendAsyncCommand('atma')

def stopatma():
    stopAsync()

def c():
    dev = '/dev/tty.OBDLinkMX-STN-SPP'
    baud = 500000
    connect(dev, baud)

    print sendCommand('atl1') #\r\n line endings
    print ati()
    print sendCommand('ath1') #headers on
    print sendCommand('ats1') #include spaces
    print sendCommand('atal') #allow long messages
    print atsp0()

if __name__ == '__main__':
    print "Loaded btcar python module."
    listSerialPorts()



