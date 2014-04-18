from serial.tools import list_ports
from controls import *
from canbus import *

def parseCANString(m):
    sender = int(m[:3], 16)
    hexmsg = int(m.replace(' ', '')[3:19], 16)
    return sender, hexmsg

def parseCANValue(hexMsg, byteIndex, mask):
    shiftedMsg = hexMsg >> (8 * (byteIndex-1))
    return shiftedMsg & mask

class Cars:

    class AbstractCar:
        def __init__(self, controlProcessors):
            self.controlProcessors = controlProcessors

        def getControlsList(self):
            return self.controlProcessors.values()

        def processMessages(self, msgs):
            for m in msgs:
                self.processMessage(m)

        """Override and implement this"""
        def processMessage(self, m):
            raise NotImplementedError()

    class SimpleCar(AbstractCar):
        def __init__(self, controlList):
            controlProcessors = {}
            for key, controlDef in controlList.items():
                controlProcessors[key] = SimpleMessageProcessor(controlDef)

            Cars.AbstractCar.__init__(self, controlProcessors)

        def processMessage(self, msg):
            key, value = msg.split(",")

            if key not in self.controlProcessors:
                print "[WARNING] Unknown message key:", key
                return

            processor = self.controlProcessors[key]
            if processor.value.setNewValue(float(value)):
                print "   %s set to %s" % (key, value)
                processor.notifyListeners()

    class CANCar(AbstractCar):
        def __init__(self, controlList):
            controls = {}
            for key, controlDef in controlList.items():
                controls[key] = CANMessageProcessor(controlDef)

            Cars.AbstractCar.__init__(self, controls)

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


class CarConnectors:

    class SimpleConnection:
        def connectToCar(self, car):
            print "Connected to Car"
            return car

        def destroy(self):
            print "Connection closed"


    class CANSerialConnection:
        def __init__(self, serial, debugAllControls):
            self.serial = serial
            self.debugAllControls = debugAllControls

            self.listSerialPorts()

        def connectToCar(self, can_car):
            self.canMonitor = Bus.CANBusMonitor(Bus.CANBus(self.serial))
            self.canMonitor.setup()
            self.canMonitor.startCANMonitor(can_car.getSenders(self.debugAllControls), can_car.processMessage)
            return can_car

        def listSerialPorts(self):
            ports = [p[0] for p in list_ports.comports()]

            print "Available serial ports:"
            for p in ports:
                print "  " + p

        def destroy(self):
            self.canMonitor.destroy()
            if self.serial:
                self.serial.close()
                print "Serial connection closed"
