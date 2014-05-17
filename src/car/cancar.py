from car import *
from canbus import CANBusMonitor, CANBus

def parseCANString(m):
    sender = int(m[:3], 16)
    hexmsg = int(m.replace(' ', '')[3:19], 16)
    return sender, hexmsg

def parseCANValue(hexMsg, byteIndex, mask):
    shiftedMsg = hexMsg >> (8 * (byteIndex-1))
    return shiftedMsg & mask

class CANCar(AbstractCar):
    class CANControlProcessor(SimpleControlProcessor):
        def __init__(self, can_control):
            SimpleControlProcessor.__init__(self, can_control)
            self.canValue = ValueTracker()

        @staticmethod
        def wrap(controlMap):
            return dict([ (key, CANCar.CANControlProcessor(controlDef))
                                for key, controlDef in controlMap.items() ])


    def __init__(self, controlList, connection):
        AbstractCar.__init__(self, CANCar.CANControlProcessor.wrap(controlList), connection)

    def getSenders(self, debugAllControls=False):
        #Debug means to follow all known inputs, even if they don't have listeners
        if debugAllControls:
            return set([c.controlDef.sender
                            for c in self.controlProcessors.values()])
        else:
            return set([c.controlDef.sender
                            for c in self.controlProcessors.values()
                            if c.listeners])

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
            if value is not None:
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

class CANSerialConnection:
    def __init__(self, serial, debugAllControls):
        self.serial = serial
        self.canMonitor = None
        self.debugAllControls = debugAllControls

    def connectToCar(self, canCar):
        self.canMonitor = CANBusMonitor(CANBus(self.serial))
        self.canMonitor.setup()
        self.canMonitor.startCANMonitor(canCar.getSenders(self.debugAllControls), canCar.processMessage)
        return canCar

    def destroy(self):
        if self.canMonitor:
            self.canMonitor.destroy()
        if self.serial:
            self.serial.close()
            print "Serial connection closed"

class CANControlDef:
    def __init__(self, name, sender, byteIndex, mask, cvmap=None, cvfunc=None):
        self.name = name
        self.sender = sender
        self.byteIndex = byteIndex
        self.mask = mask

        if cvmap is not None:
            self.correctionFx = self._CorrectedValueMap(name, cvmap).correctValue
        elif cvfunc:
            self.correctionFx = cvfunc
        else:
            raise ValueError("Either a corrected value map or function is required.")

    def senderMatches(self, sender):
        return sender == self.sender

    def getCorrectedValue(self, value):
        if value is None:
            return None
        return self.correctionFx(value)

    class _CorrectedValueMap:
        def __init__(self, name, m):
            self.map = m

        def correctValue(self, value):
            if value in self.map:
                return self.map[value]
            else:
                print "[WARNING] Unhandled value for %s: %s" % (self.name, value)
                return None