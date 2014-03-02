import sys
import time
import threading

def log(text):
    sys.stderr.write(text)

class Writer:
    def __init__(self, ser, reader):
        self.serial = ser
        self.reader = reader
        self.commandActive = False

    def sendAsyncCommand(self, command, callback):
        self.commandActive = True
        self._sendCommand(command, callback)

    def stopAsyncCommand(self):
        self._write("\r\n")
        self.reader.waitForCommand()
        self.commandActive = False

    def sendCommand(self, command):
        allentries = []
        def callback(entries):
            allentries.extend(entries)

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
        log("[OUT] " + text)
        self.serial.write(text)
        
    def destroy(self):
        if self.commandActive:
            print "Stopping active command"
            self.stopAsyncCommand()

class ReaderThread(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = False

        self.serial = ser
        self.async = _AsyncCommand()

    def setCurrentCommand(self, command, callback):
        self.async.set(command, callback)

    def waitForCommand(self):
        self.async.waitFor()

    def kill(self):
        self.running = False

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
#                if buffer.endswith("BUFFER FULL\r\n\r\n>"):
#                    print "Buffer full! Aborting."
#                return False

                entries = buffer.split('\r\n')

                if len(entries) - 1 > 0:
                    self._handleData(entries[:len(entries) - 1])
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

