import sys
import time
import threading
import re

DEBUG = False

def log(text):
    if DEBUG:
        sys.stderr.write(text)

class Bus:

    class CANBus:
        def __init__(self, ser, reader=None):
            self.serial = ser
            self.commandActive = False

            if reader:
                self.reader = reader
            else:
                self.reader = ReaderThread(self.serial)
                self.reader.start()

        def sendAsyncCommand(self, command, callback):
            self.commandActive = True
            self._sendCommand(command, callback)

        def stopAsyncCommand(self):
            if self.commandActive:
                print "Stopping active command"
                self._write("\r\n")
                self.reader.waitForCommand()
                self.commandActive = False

        def sendCommand(self, command):
            allentries = []
            def callback(entry):
                if entry != ">": #Skip recording prompt
                    allentries.append(entry)

            self._sendCommand(command, callback)
            self.reader.waitForCommand()

            return allentries

        def _sendCommand(self, command, callback):
            self.reader.setCurrentCommand(command, callback)
            self._writeln(command)

        def _writeln(self, text):
            self._write(text)
            log("\n")
            self.serial.write("\r\n")

        def _write(self, text):
            sys.stderr.write("[OUT] " + text + "\n")#JRTODO
    #        log("[OUT] " + text)
            self.serial.write(text)

        def destroy(self):
            self.stopAsyncCommand()
            self.reader.destroy()

    class DummyCANBus:
        def __init__(self, ser, reader):
            pass

        def sendAsyncCommand(self, command, callback):
            pass

        def stopAsyncCommand(self):
            pass

        def sendCommand(self, command):
            pass

        def destroy(self):
            pass

    class CANBusMonitor:
        def __init__(self, can):
            self.can = can

        def setup(self):
            self.can.sendCommand('atl1') #\r\n line endings
            self.can.sendCommand('ati')
            self.can.sendCommand('ath1') #headers on
            self.can.sendCommand('ats1') #include spaces
            self.can.sendCommand('atal') #allow long messages
            self.can.sendCommand('atsp6') #set to protocol 6, (CAN 11bit ID, 500kbaud)

        def startCANMonitor(self, senderIds, messageCallback):
            #Clear filters
            self.can.sendCommand('stfcp') #clear pass filters
            self.can.sendCommand('stfcb') #clear blocking filters
            self.can.sendCommand('stfcfc') #clear flow control filters

            #Add filters
            for id in senderIds:
                self.can.sendCommand('stfap %s,fff' % hex(id)[2:].zfill(3))

            self.can.sendAsyncCommand('stm', messageCallback)

        def stopCANMonitor(self):
            self.can.stopAsyncCommand()

        def destroy(self):
            self.can.destroy()

class ReaderThread(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = False

        self.serial = ser
        self.async = self._AsyncCommand()

    def setCurrentCommand(self, command, callback):
        self.async.set(command, callback)

    def waitForCommand(self):
        self.async.waitFor()

    def kill(self):
        self.running = False

    def destroy(self):
        print "Killing reader thread and waiting for it to die."
        self.kill()
        self.join()
        print "Dead."

    def _handleData(self, entries):
        if not entries:
            return

        for e in entries:
            self.async.process(e)

    def run(self):
        self.running = True

        buffer = ""
        while self.running:
            if self.serial.inWaiting():
                text = self.serial.read(self.serial.inWaiting())

                buffer += text

                entries = re.split(r'\r?\n?', buffer)


                endsWithNewline = len(entries) and entries[-1] in ("", ">")
                if endsWithNewline:
                    toProcess = entries[:len(entries)]
                    self._handleData(toProcess)
                    buffer = ""
                else:
                    if len(entries) - 1 > 0:
                        toProcess = entries[:len(entries)-1]
                        self._handleData(toProcess)
                        buffer = entries[-1]
                    elif len(entries):
                        buffer = entries[-1]

            time.sleep(.001)


    class _AsyncCommand:
        def __init__(self):
            self._reset()

        def _reset(self):
            self.found = False
            self.running = False
            self.command = None
            self.callback = None

        def _done(self):
            self._reset()

        def set(self, command, callback):
            if self.running:
                raise ValueError("Command in progress. Can't change this.")

            self.found = False
            self.running = True
            self.command = command
            self.callback = callback

        def process(self, e):
            if self.running:

                #Skip blank lines
                if not len(e):
                    return

                log(e + '\n')

                if not self.found:

                    #If we see the command come through, start 'recording'
                    if self.command == e:
                        self.found = True
                else:
                    #Call the callback if it exists
                    if self.callback:
                        self.callback(e)

                    #Command is finished when we get the prompt
                    if ">" == e:
                        self._done()

            else:
                log("[MAGIC DATA]" + e + "\n")

        def waitFor(self):
            while self.running:
                time.sleep(.001)

