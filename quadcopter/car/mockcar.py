import sys
import serial
import time
import threading

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

class ReaderThread(SerialThread):
    def __init__(self, ser):
        SerialThread.__init__(self, ser)
        self.daemon = True
        self.running = False

        self.activeOutputThread = None

    def kill(self):
        self.running = False

    def handleCommands(self, commands):
        for c in commands:
            #If there's a command already running, the incoming text
            #doesn't matter, just the newline
            if self.activeOutputThread:
                c = ""
                self.activeOutputThread.kill()
                self.activeOutputThread.join()
                self.activeOutputThread = None

                self.writeln(c)
                self.writeln(">")

            else:
                self.writeln(c)

                uc = c.upper()
                if uc == "ATI":
                    self.writeln("ELM 1.0.37a")
                elif uc == "STM":
                    self.activeOutputThread = MonitorOutputThread(self.serial)
                    self.activeOutputThread.start()
                    return
                else:
                    self.writeln('OK')

                self.writeln(">")

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
    def __init__(self, ser):
        SerialThread.__init__(self, ser)
        self.running = False

    def kill(self):
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            self.writeln("39E 00 00 00 00 00 00 00 00")
            time.sleep(2)
            self.writeln("39E 00 00 20 00 00 00 00 00")
            self.writeln("228 00 00 00 00 00 00 00 00")
            time.sleep(2)




if __name__ == '__main__':
    ser = serial.Serial('/tmp/fake1', 9600)
    readerThread = ReaderThread(ser)
    readerThread.start()

    while True:
        time.sleep(.1)

