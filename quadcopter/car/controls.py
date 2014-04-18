
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

class AbstractMessageProcessor:
    def __init__(self, controlDef):
        self.listeners = []
        self.value = ValueTracker()
        self.controlDef = controlDef

    def registerListener(self, listener):
        self.listeners.append(listener)

    def notifyListeners(self):
        for l in self.listeners:
            l(self.controlDef.name, self.value.value, self.value.prev)

    def setNewValue(self, newValue):
        return self.value.setNewValue(newValue)

    def getValue(self):
        return self.value.value

class SimpleMessageProcessor(AbstractMessageProcessor):
    def __init__(self, controlDef):
        AbstractMessageProcessor.__init__(self, controlDef)

class CANMessageProcessor(AbstractMessageProcessor):
    def __init__(self, can_control):
        AbstractMessageProcessor.__init__(self, can_control)

        self.canValue = ValueTracker()

class ControlDefs:

    class SimpleControlDef:
        def __init__(self, name):
            self.name = name

    class CANControlDef:
        def __init__(self, name, sender, byteIndex, mask, cvmap=None, cvfunc=None):
            self.name = name
            self.sender = sender
            self.byteIndex = byteIndex
            self.mask = mask

            if cvmap is not None:
                self.correctionFx = self._CorrectedValueMap(name, cvmap).correctValue
            elif cvfunc is not None:
                self.correctionFx = cvfunc
            else:
                raise ValueError("Either a corrected value map or function is required.")

        def senderMatches(self, sender):
            return sender == self.sender

        def getCorrectedValue(self, value):
            if value == None:
                return None

            try:
                return self.correctionFx(value)
            except ValueError:
                print "[WARNING] Unhandled value for %s: %s" % (self.name, value)
                return None

        class _CorrectedValueMap:
            def __init__(self, name, m):
                self.map = m

            def correctValue(self, value):
                if value in self.map:
                    return self.map[value]
                else:
                    raise ValueError()
