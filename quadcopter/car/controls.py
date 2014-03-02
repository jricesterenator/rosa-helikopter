import sys

def parseCANValue(hexMsg, byteIndex, mask):
    shiftedMsg = hexMsg >> (8 * (byteIndex-1))
    return shiftedMsg & mask

class ValueTracker:
    def __init__(self):
        self.value = None
        self.prev = None

    def _isNewValue(self, newValue):
        return self.value != newValue

    def _isSameValue(self, newValue):
        return self.value == newValue

    def setNewValue(self, newValue):
        if self._isNewValue(newValue):
            self.prev = self.value
            self.value = newValue
            return True
        else:
            return False

class BaseControl:
    def __init__(self, name):
        self.name = name
        self.listeners = []

        self.value = ValueTracker()

    def registerListener(self, listener):
        self.listeners.append(listener)

    def notifyListeners(self):
        for l in self.listeners:
            l(self)

    def setNewValue(self, newValue):
        return self.value.setNewValue(newValue)

    def getValue(self):
        return self.value.value


"""
This class should let us create, use, notify, car controls
without having to know CAN messages.
"""
class GenericControl(BaseControl):
    def __init__(self, name):
        BaseControl.__init__(self, name)

"""This class processes CAN messages and notifies listeners"""
class CANControl(BaseControl):
    def __init__(self, name, sender, byteIndex, mask, cvmap=None, cvfunc=None):
        BaseControl.__init__(self, name)

        self.can = ValueTracker()

        self.sender = sender
        self.byteIndex = byteIndex
        self.mask = mask

        if cvmap:
            self.correctionFx = self._CorrectedValueMap(cvmap).correctValue
        elif cvfunc:
            self.correctionFx = cvfunc
        else:
            raise ValueError("Either a corrected value map or function is required.")

    def processCANMessage(self, sender, hexmsg):
        if self._senderMatches(sender):
            canValue = self._parseCANValue(hexmsg)

            #JRTODO: If I need to sync the value changes between CAN and real,
            #JRTODO: only set the CAN value after processing the real value.
            #JRTODO: However, I don't think it will be a problem.

            #If CAN value changed, update the corrected value
            if self.can.setNewValue(canValue):

                #Print updated CAN value info
                self._printChangeInfo(self.can.prev, canValue)

                #Update converted value
                convertedValue = self._getCorrectedValue(canValue)
                if self.setNewValue(convertedValue):

                    #Notify
                    self.notifyListeners()

    def _senderMatches(self, sender):
        return sender == self.sender

    def _getCorrectedValue(self, value):
        if value == None:
            return None

        try:
            return self.correctionFx(value)

        except ValueError:
            msg = "[WARNING] Unsure of value for %s: %s" %\
                  (self.name, self._getPrintableCANValue(value))
            print msg
            return None

    def _parseCANValue(self, hexmsg):
        return parseCANValue(hexmsg, self.byteIndex, self.mask)

    def _printChangeInfo(self, prevValue, newValue):

        prevCorrected = self._getCorrectedValue(prevValue)
        newCorrected = self._getCorrectedValue(newValue)

        print "[INFO] %s changed from %s to %s (%s --> %s): %s" %\
              (self.name,
               self._getPrintableCANValue(prevValue),
               self._getPrintableCANValue(newValue),
               prevCorrected,
               newCorrected,
               newCorrected)

    def _getPrintableCANValue(self, value):
        string = "NOT_SET"
        if value != None:
            string = hex(value)
        return string

    class _CorrectedValueMap:
        def __init__(self, m):
            self.map = m

        def correctValue(self, value):
            if value in self.map:
                return self.map[value]
            else:
                raise ValueError()


def when(self, *args):
    return _When(self, *args)

class _When:
    def __init__(self, control, cmpFx):
        self.control = control
        self.cmpFx = cmpFx
        self.callback = None

    def then(self, callback):
        self.callback = callback
        self.control.registerListener(self._onThen)

    def _onThen(self, control):
        correctedValue = control.getValue()
        if self.cmpFx(correctedValue):
            self.callback(correctedValue)

def eq(value):
    return lambda x : value == x

def any():
    return lambda x : True

def echo(name):
    return lambda x : sys.stderr.write(name + ": " + str(x) + "\n")

