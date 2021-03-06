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

            if CAN_MESSAGES and len(msg):
                try:
                    sender = int(msg[:3], 16)
                except ValueError:
                    print "[ERROR] Invalid CAN message, not sending.", msg
                    continue

                allowed = False
                for id, mask in self.data.allowedSenders:
                    if (id & mask) == (sender & mask):
                        allowed = True
                        break

                if allowed:
                    self.writeln(msg)
                    time.sleep(PLAYBACK_SPEED)
                else:
                    print "[DEBUG] Skipping message because it's not an allowed sender.", msg
            else:
                self.writeln(msg)
                time.sleep(PLAYBACK_SPEED)


if __name__ == '__main__':
    ser = serial.Serial('/tmp/fake1', 9600)
    readerThread = ReaderThread(ser)
    readerThread.start()

    print "Usage: %s [-s]" % sys.argv[0]
    print "  -s Use simple mode (Ex: 'handbrake,0' instead of CAN)"
    print "     By default, CAN is used."

    if len(sys.argv) > 1 and sys.argv[1] == '-s':
        CAN_MESSAGES=False
    else:
        CAN_MESSAGES=True

    while True:
        time.sleep(.1)

