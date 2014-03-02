import sys

def parseMessageString(m):
    sender = int(m[:3], 16)
    hexmsg = int(m.replace(' ', '')[3:19], 16)

    return sender, hexmsg


#JRTODO: Work off a queue instead of calling processMessages
class ControlProcessor:

    def __init__(self, controls):
        self.controls = controls

    def processMessage(self, m):
        self.processMessages([m])

    def processMessages(self, msgs):
        for m in msgs:
            try:
                sender, hexmsg = parseMessageString(m)

            except ValueError:
                print "[WARNING]", m, "is not a CAN message."
                continue

            except TypeError:
                print "[WARNING]", m, "is not a CAN message."
                continue

            self._processMessage(sender, hexmsg)

    def _processMessage(self, sender, hexmsg):

        for control in self.controls.getControls():

            if control.matches(sender):
                value = control.parseValue(hexmsg)
                control.onControlChange(value)


class Control:

    def __init__(self, controlDef, listeners=None):
        self.controlDef = controlDef
        self.name = controlDef.name

        self.prevValue = None
        self.value = None

        if listeners:
            self.listeners = listeners
        else:
            self.listeners = []

    def onControlChange(self, newValue):

        #Value not changed?
        if self.value == newValue:
            return

        #Set the new value
        self.prevValue = self.value
        self.value = newValue

        self.printChangeInfo(self.prevValue, newValue)

        #Notify listeners
        for listener in self.listeners:
            listener(self)

    def getPrintableValue(self, value):
        string = "NOT_SET"
        if value != None:
            string = hex(value)
        return string

    def matches(self, sender):
        return sender == self.controlDef.sender

    def parseValue(self, hexMsg):
        offsetBytes = self.controlDef.byteIndex-1
        offsetBits = 8 * offsetBytes
        shiftedMsg = hexMsg >> offsetBits
        value = shiftedMsg & self.controlDef.mask
        return value

    def getCurrCorrectedValue(self):
        return self.getCorrectedValue(self.value)

    def getCorrectedValue(self, value):
        if value == None:
            return None

        try:
            return self.controlDef.correctionFx(value)

        except ValueError:
            msg = "[WARNING] Unsure of value for %s: %s" %\
                  (self.name, self.getPrintableValue(value))
            print msg
            return None

    def printChangeInfo(self, prevValue, newValue):

        prevCorrected = self.getCorrectedValue(prevValue)
        newCorrected = self.getCorrectedValue(newValue)

        print "[INFO] %s changed from %s to %s (%s --> %s): %s" %\
              (self.name,
               self.getPrintableValue(prevValue),
               self.getPrintableValue(newValue),
               prevCorrected,
               newCorrected,
               newCorrected)


class ControlDef:
    def __init__(self, name, sender, byteIndex, mask, cvmap=None, cvfunc=None):
        self.name = name
        self.sender = sender
        self.byteIndex = byteIndex
        self.mask = mask

        if cvmap != None:
            self.correctionFx = _CorrectedValueMap(cvmap).correctValue
        elif cvfunc != None:
            self.correctionFx = cvfunc
        else:
            raise ValueError("Either a corrected value map or function is required.")



class Controls:

    def __init__(self):
        self.controlMap = {}
        for k,cdef in CONTROL_DEFS.items():
            self.controlMap[k] = Control(cdef)

    def activeSenders(self):
        ids = set()
        for v in self.controlMap.values():
            if v.listeners:
                ids.add(v.controlDef.sender)
        return ids

    def addListener(self, controlDef, listener):
        self.controlMap[controlDef].listeners.append(listener)

    def getControls(self):
        return self.controlMap.values()

    def when(self, *args):
        return _When(self, *args)

class _When:
    def __init__(self, controls, controlDef, cmpFx):
        self.controls = controls
        self.controlDef = controlDef
        self.cmpFx = cmpFx
        self.callback = None

    def then(self, callback):
        self.callback = callback
        listener = _ControlListener(self.cmpFx, self.callback).onControlChange
        self.controls.addListener(self.controlDef, listener)

class _ControlListener:
    def __init__(self, cmpFx, callback):
        self.cmpFx = cmpFx
        self.callback = callback

    def onControlChange(self, control):
        correctedValue = control.getCurrCorrectedValue()
        if self.cmpFx(correctedValue):
            self.callback(correctedValue)

class _CorrectedValueMap:
    def __init__(self, m):
        self.map = m

    def correctValue(self, value):
        if value in self.map:
            return self.map[value]
        else:
            raise ValueError()

def eq(value):
    return lambda x : value == x

def any():
    return lambda x : True

def echo(name):
    return lambda x : sys.stderr.write(name + ": " + str(x) + "\n")

def steering1(value):
    if value > 60000: #JRTODO: more official way to come up with this number?
        offcenter = value - 65536
    else:
        offcenter = value
    deg = offcenter/10 #convert 10ths of a degree to degree
    return deg
        

""" Name, Sender, Byte #, Mask """
CONTROL_DEFS = {
    'reverse'  : ControlDef("Reverse",     sender=0x39E, byteIndex=5, mask=0xF0, cvmap={0x00:0, 0x10:1}),
    'handbrake': ControlDef("Handbrake",   sender=0x39E, byteIndex=6, mask=0xF0, cvmap={0x00:0, 0x20:1}),
    'neutral'  : ControlDef("In Neutral",  sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:1, 0x04:0}),
    'ingear'   : ControlDef("In Gear",     sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:0, 0x04:1}),
    'brake'    : ControlDef("Brake",       sender=0x190, byteIndex=6, mask=0xF0, cvmap={0x40:1, 0x00:0}),
    'clutch'   : ControlDef("Clutch",      sender=0x050, byteIndex=5, mask=0x0F, cvmap={0x00:0, 0x01:0, 0x02:1}),
    'steering1': ControlDef("Steering1",   sender=0x082, byteIndex=5, mask=0xFFFF, cvfunc=steering1)
}