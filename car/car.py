import thread

class AbstractCar:
    def __init__(self, controlProcessors, connection):
        self.controlProcessors = controlProcessors
        self.connection = connection

    def connect(self):
        self.connection.connectToCar(self)

    def disconnect(self):
        self.connection.destroy()

    def registerListener(self, callback):
        for processor in self.getControlsList():
            processor.registerListener(callback)

    def getControlsList(self):
        return self.controlProcessors.values()

    def processMessages(self, msgs):
        for m in msgs:
            self.processMessage(m)

    """Override and implement this"""
    def processMessage(self, m):
        raise NotImplementedError()


class SimpleCar(AbstractCar):
    def __init__(self, controlList, connection):
        AbstractCar.__init__(self, SimpleControlProcessor.wrap(controlList), connection)

    def getSenders(self, debug):
        return []

    def processMessage(self, msg):
        if ',' not in msg:
            print '[ERROR] Invalid simple car message (%s). ' \
                  'Expecting: <input>,<value>.' % msg
            return
        key, value = msg.split(",")

        if key not in self.controlProcessors:
            print "[WARNING] Unknown message key:", key
            return

        processor = self.controlProcessors[key]
        if processor.value.setNewValue(float(value)):
            print "   %s set to %s" % (key, value)
            processor.notifyListeners()


class SimpleConnection:
    def commandReader(self, callback):
        print
        while True:
            m = raw_input("Enter Simulated Bus Message: ")
            callback(m.strip())

    def connectToCar(self, car):
        print "Connected to Car"
        thread.start_new_thread(self.commandReader, (car.processMessage,))
        return car

    def destroy(self):
        print "Connection closed"


class SimpleControlProcessor:
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

    @staticmethod
    def wrap(controlMap):
        return dict([ (key, SimpleControlProcessor(controlDef))
                      for key, controlDef in controlMap.items() ])


class SimpleControlDef:
    def __init__(self, name):
        self.name = name


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