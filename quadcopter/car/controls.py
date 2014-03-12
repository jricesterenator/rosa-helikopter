import sys

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

class AbstractValueHandler:
    def __init__(self, control_def):
        self.listeners = []
        self.value = ValueTracker()
        self.control_def = control_def

    def registerListener(self, listener):
        self.listeners.append(listener)

    def notifyListeners(self):
        for l in self.listeners:
            l(self.control_def.name, self.value.value, self.value.prev)

    def setNewValue(self, newValue):
        return self.value.setNewValue(newValue)

    def getValue(self):
        return self.value.value

class GenericValueHandler(AbstractValueHandler):
    def __init__(self, control_def):
        AbstractValueHandler.__init__(self, control_def)

class CANMessageProcessor(AbstractValueHandler):
    def __init__(self, can_control):
        AbstractValueHandler.__init__(self, can_control)

        self.canValue = ValueTracker()



class ControlDefs:

    class GenericControlDef:
        def __init__(self, name):
            self.name = name

    class CANControlDef:
        def __init__(self, name, sender, byteIndex, mask, cvmap=None, cvfunc=None):
            self.name = name
            self.sender = sender
            self.byteIndex = byteIndex
            self.mask = mask

            if cvmap is not None:
                self.correctionFx = self._CorrectedValueMap(cvmap).correctValue
            elif cvfunc is not None:
                self.correctionFx = cvfunc
            else:
                raise ValueError("Either a corrected value map or function is required.")

        def senderMatches(self, sender):
            return sender == self.sender

        def getCorrectedValue(self, value):
            if value == None:
                return None
            return self.correctionFx(value)

        class _CorrectedValueMap:
            def __init__(self, m):
                self.map = m

            def correctValue(self, value):
                if value in self.map:
                    return self.map[value]
                else:
                    raise ValueError()
