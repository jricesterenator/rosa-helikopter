
def parseCANString(m):
    sender = int(m[:3], 16)
    hexmsg = int(m.replace(' ', '')[3:19], 16)
    return sender, hexmsg

class VirtualCar:
    def __init__(self, controlMap):
        self.controlMap = controlMap

    def getSenders(self):
        ids = set()
        for control in self.controlMap.values():
            if control.listeners:
                ids.add(control.sender)
        return ids

    def getControls(self):
        return self.controlMap.values()

    def processMessages(self, msgs):
        for m in msgs:
            self.processMessage(m)

    def processMessage(self, m):
        pass

class SimpleCar(VirtualCar):
    def __init__(self, controlMap):
        VirtualCar.__init__(self, controlMap)

    def processMessage(self, (control, msg)):
        control.setNewValue(msg)
        control.notifyListeners()

#JRTODO: Work off a queue instead of calling processMessages?
class CANCar(VirtualCar):
    def __init__(self, controlMap):
        VirtualCar.__init__(self, controlMap)

    def processMessage(self, m):
        try:
            sender, hexmsg = parseCANString(m)

        except ValueError:
            print "[WARNING]", m, "is not a CAN message."
            return

        except TypeError:
            print "[WARNING]", m, "is not a CAN message."
            return

        self._processMessage(sender, hexmsg)

    def _processMessage(self, sender, hexmsg):
        for control in self.getControls():
            control.processCANMessage(sender, hexmsg)
