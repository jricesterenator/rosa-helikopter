from controls import *
from canbus import *
from car import AbstractCar

def parseCANString(m):
    sender = int(m[:3], 16)
    hexmsg = int(m.replace(' ', '')[3:19], 16)
    return sender, hexmsg

def parseCANValue(hexMsg, byteIndex, mask):
    shiftedMsg = hexMsg >> (8 * (byteIndex-1))
    return shiftedMsg & mask

class CANSerialConnection:
    def __init__(self, serial, debugAllControls):
        self.serial = serial
        self.debugAllControls = debugAllControls


    def connectToCar(self, can_car):
        self.canMonitor = Bus.CANBusMonitor(Bus.CANBus(self.serial))
        self.canMonitor.setup()
        self.canMonitor.startCANMonitor(can_car.getSenders(self.debugAllControls), can_car.processMessage)
        return can_car

    def destroy(self):
        self.canMonitor.destroy()
        if self.serial:
            self.serial.close()
            print "Serial connection closed"

class CANCar(AbstractCar):
    def __init__(self, controlList, connection):
        controls = {}
        for key, controlDef in controlList.items():
            controls[key] = CANControlProcessor(controlDef)

        AbstractCar.__init__(self, controls, connection)

    def getSenders(self, debugAllControls=False):
        if debugAllControls:#follow all inputs, even if they don't have listeners
            ids = set()
            for control in self.controlProcessors.values():
                ids.add(control.controlDef.sender)
            return ids
        else:
            ids = set()
            for control in self.controlProcessors.values():
                if control.listeners:
                    ids.add(control.sender)
            return ids

    def processMessage(self, m):
        try:
            sender, hexmsg = self._parseCANString(m)

        except ValueError:
            print "[WARNING]", m, "is not a CAN message."
            return

        except TypeError:
            print "[WARNING]", m, "is not a CAN message."
            return

        for processor in self.controlProcessors.values():
            self._processCANMessage(processor, sender, hexmsg)

    def _parseCANString(self, m):
        return parseCANString(m)

    def _processCANMessage(self, processor, sender, hexmsg):
        controlDef = processor.controlDef
        if controlDef.senderMatches(sender):
            canValue = self._parseCANValue(hexmsg, controlDef.byteIndex, controlDef.mask)

            #JRTODO: If I need to sync the value changes between CAN and real,
            #JRTODO: only set the CAN value after processing the real value.
            #JRTODO: However, I don't think it will be a problem.

            #If CAN value changed, update the corrected value
            if processor.canValue.setNewValue(canValue):

                #Print updated CAN value info
                self._printChangeInfo(controlDef, processor.canValue.prev, canValue)

                #Update converted value
                convertedValue = controlDef.getCorrectedValue(canValue)
                if processor.setNewValue(convertedValue):
                    processor.notifyListeners()


    def _parseCANValue(self, hexMsg, byteIndex, mask):
        return parseCANValue(hexMsg, byteIndex, mask)

    def _printChangeInfo(self, controlDef, prevValue, newValue):

        def _getPrintableCANValue(value):
            string = "NOT_SET"
            if value != None:
                string = "0x" + ("%x" % value).upper()
            return string

        prevCorrected = controlDef.getCorrectedValue(prevValue)
        newCorrected = controlDef.getCorrectedValue(newValue)

        print "[INFO] %s changed from %s to %s (%s --> %s): %s" %\
              (controlDef.name,
               _getPrintableCANValue(prevValue),
               _getPrintableCANValue(newValue),
               prevCorrected,
               newCorrected,
               newCorrected)


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


class CANControlProcessor(AbstractControlProcessor):
    def __init__(self, can_control):
        AbstractControlProcessor.__init__(self, can_control)
        self.canValue = ValueTracker()