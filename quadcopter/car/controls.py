
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

class AbstractControlProcessor:
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

class SimpleControlProcessor(AbstractControlProcessor):
    def __init__(self, controlDef):
        AbstractControlProcessor.__init__(self, controlDef)


class ControlDefs:
    class SimpleControlDef:
        def __init__(self, name):
            self.name = name

