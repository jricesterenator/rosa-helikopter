import sys
import serial
import time
import threading

PLAYBACK_SPEED=.5 #seconds delay between messages

def log(text):
    sys.stderr.write(text)

class SerialThread(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.daemon = True
        self.serial = ser

    def writeln(self, text):
        self.write(text)

        log("\n")
        self.serial.write("\r\n")

    def write(self, text):
        log(text)
        self.serial.write(text)

class DataObj:
    def __init__(self):
        self.allowedSenders = []

class ReaderThread(SerialThread):
    def __init__(self, ser):
        SerialThread.__init__(self, ser)
        self.daemon = True
        self.running = False

        self.activeOutputThread = None

        self.data = DataObj()

    def kill(self):
        self.running = False

    def handleCommands(self, commands):
        for c in commands:
            #If there's a command already running, the incoming text
            #doesn't matter, just the newline
            if self.activeOutputThread:
                self.activeOutputThread.kill()
                self.activeOutputThread.join()
                self.activeOutputThread = None
                self.write(">")

            else:
                self.writeln(c)

                uc = c.upper()
                if uc == "ATI": #request device info
                    self.writeln("ELM 1.0.37a")
                elif uc == "ATRV": #battery voltage
                    self.writeln("13.8V")
                elif uc.startswith("STFCP"): #clear senders
                    self.data.allowedSenders = []
                elif uc.startswith("STFAP"): #allowed senders
                    #JRTODO do the masking properly
                    id,mask = uc[len('STFAP '):].split(',')
                    idhex = int(id, 16)
                    maskhex = int(mask, 16)
                    self.data.allowedSenders.append((idhex, maskhex))

                elif uc == "STM": #start monitor
                    self.activeOutputThread = MonitorOutputThread(self.serial, self.data)
                    self.activeOutputThread.start()
                    return
                else:
                    self.writeln('OK')

                self.write(">")

    def run(self):
        self.running = True

        buffer = ""
        while self.running:
            if self.serial.inWaiting():
                text = self.serial.read(self.serial.inWaiting())

                buffer += text
                entries = buffer.split('\r\n')

                if len(entries) - 1 > 0:
                    self.handleCommands(entries[:len(entries) - 1])
                    buffer = entries[-1]

            time.sleep(.1)


class MonitorOutputThread(SerialThread):
    def __init__(self, ser, data):
        SerialThread.__init__(self, ser)
        self.running = False
        self.data = data

    def kill(self):
        self.running = False

    def run(self):
        self.running = True

        print "[Enter the messages to send back from the car]"
        while self.running:

            msg = raw_input("::").strip()
            sender = int(msg[:3], 16)

            allowed = False
            for id, mask in self.data.allowedSenders:
                if (id & mask) == (sender & mask):
                    allowed = True
                    break

            if allowed or not len(msg):
                self.writeln(msg)
                time.sleep(PLAYBACK_SPEED)
            else:
                print "[DEBUG] Skipping message because it's not an allowed sender.", msg


if __name__ == '__main__':
    ser = serial.Serial('/tmp/fake1', 9600)
    readerThread = ReaderThread(ser)
    readerThread.start()

    while True:
        time.sleep(.1)

