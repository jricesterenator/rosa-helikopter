__author__ = 'jjrice'

import unittest
from quadcopter.car.controls import *

def hexmsg(hexString):
    sender, hexmsg = parseMessageString(hexString)
    return hexmsg

class ListenerAssertion:

    def __init__(self, testClass):
        self.wasCalled = False
        self.testClass = testClass

    def onListener(self, control):
        self.wasCalled = True

        self.testClass.assertEqual(self.name, control.name)
        self.testClass.assertEqual(self.prevValue, control.prevValue)
        self.testClass.assertEqual(self.value, control.value)

class GenericControlsTest(unittest.TestCase):

    def setUp(self):
        self.controlDef = ControlDef("Custom Control", sender=0xA3, byteIndex=3, mask=0xFF, cvfunc=lambda x:2*x)
        self.c = Control(self.controlDef)

    def testControl_SenderMatches(self):
        self.assertTrue(self.c.matches(0xA3))

    def testControl_SenderDoesntMatch(self):
        self.assertFalse(self.c.matches(0x205))

    def testControl_ParseOff(self):
        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testControl_ParseOn(self):
        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 20 00 00"))
        self.assertEqual(0x20, val)

    def testControl_ParseOnWhenOtherByteSet_PermissiveMask(self):
        self.controlDef.mask = 0xFF
        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 28 00 00"))
        self.assertEqual(0x28, val)

    def testControl_ParseOnWhenOtherByteSet_RestrictiveMask(self):
        self.controlDef.mask = 0xF0
        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 28 00 00"))
        self.assertEqual(0x20, val)

    def testControl_CorrectedValue_Off(self):
        self.assertEqual(0, self.c.getCorrectedValue(0x00))

    def testControl_CorrectedValue_On(self):
        self.assertEqual(2*0x20, self.c.getCorrectedValue(0x20))

    def testControl_CorrectedValue_NotSet(self):
        self.assertEqual(None, self.c.getCorrectedValue(None))

    def testControl_CorrectedValue_UnknownValue(self):
        #Pretend that getCorrectedValue returns a ValueError because it can't translate the value
        def raiseError(value):
            raise ValueError

        self.controlDef.correctionFx = raiseError
        self.assertEqual(None, self.c.getCorrectedValue(0x28))

    def testControl_ListenersCalled(self):
        la1 = ListenerAssertion(self)
        la2 = ListenerAssertion(self)
        self.c.listeners = [la1.onListener, la2.onListener]

        #Test value changing from NOT_SET to 0x20
        la1.name = "Custom Control"
        la1.prevValue = None
        la1.value = 0x20

        la2.name = "Custom Control"
        la2.prevValue = None
        la2.value = 0x20

        self.c.onControlChange(0x20)
        self.assertTrue(la1.wasCalled)
        self.assertTrue(la2.wasCalled)


        #Test value changing from 0x20 to 0x00
        la1.wasCalled = False
        la1.prevValue = 0x20
        la1.value = 0x00

        la2.wasCalled = False
        la2.prevValue = 0x20
        la2.value = 0x00

        self.c.onControlChange(0x00)

        self.assertTrue(la1.wasCalled)
        self.assertTrue(la2.wasCalled)

class BrakeTest(unittest.TestCase):

    def setUp(self):
        self.c = Control(CONTROL_DEFS['brake'])

    def testBrake_SenderMatches(self):
        self.assertTrue(self.c.matches(0x190))

    def testBrake_ParseBrakeNotActive(self):
        val = self.c.parseValue(hexmsg("190 00 00 00 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testBrake_ParseBrakeActive(self):
        val = self.c.parseValue(hexmsg("190 00 00 40 00 00 00 00 00"))
        self.assertEqual(0x40, val)

    def testBrake_ParseBrakeActiveWhenOtherByteSet_IgnoresOtherByte(self):
        val = self.c.parseValue(hexmsg("190 00 00 46 00 00 00 00 00"))
        self.assertEqual(0x40, val)

    def testBrake_ParseBrakeNotActiveWhenOtherByteSet_IgnoresOtherByte(self):
        val = self.c.parseValue(hexmsg("190 00 00 06 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testBrake_CorrectedValue_BrakeActive(self):
        self.assertEqual(1, self.c.getCorrectedValue(0x40))

    def testBrake_CorrectedValue_BrakeNotActive(self):
        self.assertEqual(0, self.c.getCorrectedValue(0x00))

    def testBrake_CorrectedValue_NotSet(self):
        self.assertEqual(None, self.c.getCorrectedValue(None))

    def testBrake_CorrectedValue_UnknownValue(self):
        self.assertEqual(None, self.c.getCorrectedValue(0x28))

class HandbrakeTest(unittest.TestCase):

    def setUp(self):
        self.c = Control(CONTROL_DEFS['handbrake'])

    def testHandbrake_SenderMatches(self):
        self.assertTrue(self.c.matches(0x39E))

    def testHandbrake_ParseOff(self):
        val = self.c.parseValue(hexmsg("39E 00 00 00 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testHandbrake_ParseOn(self):
        val = self.c.parseValue(hexmsg("39E 00 00 20 00 00 00 00 00"))
        self.assertEqual(0x20, val)

    def testHandbrake_ParseOnWhenOtherByteSet_IgnoresOtherByte(self):
        val = self.c.parseValue(hexmsg("39E 00 00 28 00 00 00 00 00"))
        self.assertEqual(0x20, val)

    def testHandbrake_CorrectedValue_Off(self):
        self.assertEqual(0, self.c.getCorrectedValue(0x00))

    def testHandbrake_CorrectedValue_On(self):
        self.assertEqual(1, self.c.getCorrectedValue(0x20))

    def testHandbrake_CorrectedValue_NotSet(self):
        self.assertEqual(None, self.c.getCorrectedValue(None))

    def testHandbrake_CorrectedValue_UnknownValue(self):
        self.assertEqual(None, self.c.getCorrectedValue(0x28))

class InGearTest(unittest.TestCase):

    def setUp(self):
        self.c = Control(CONTROL_DEFS['ingear'])

    def testInGear_SenderMatches(self):
        self.assertTrue(self.c.matches(0x228))

    def testInGear_ParseNotInGear(self):
        val = self.c.parseValue(hexmsg("228 00 00 00 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testInGear_ParseInGear(self):
        val = self.c.parseValue(hexmsg("228 00 04 00 00 00 00 00 00"))
        self.assertEqual(0x04, val)

    def testInGear_ParseInGearWhenOtherByteSet_IgnoresOtherByte(self):
        val = self.c.parseValue(hexmsg("228 00 64 00 00 00 00 00 00"))
        self.assertEqual(0x04, val)

    def testInGear_ParseNotInGearWhenOtherByteSet_IgnoresOtherByte(self):
        val = self.c.parseValue(hexmsg("228 00 60 00 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testInGear_CorrectedValue_InGear(self):
        self.assertEqual(1, self.c.getCorrectedValue(0x04))

    def testInGear_CorrectedValue_NotInInGear(self):
        self.assertEqual(0, self.c.getCorrectedValue(0x00))

    def testInGear_CorrectedValue_NotSet(self):
        self.assertEqual(None, self.c.getCorrectedValue(None))

    def testInGear_CorrectedValue_UnknownValue(self):
        self.assertEqual(None, self.c.getCorrectedValue(0x28))

class NeutralTest(unittest.TestCase):

    def setUp(self):
        self.c = Control(CONTROL_DEFS['neutral'])

    def testNeutral_SenderMatches(self):
        self.assertTrue(self.c.matches(0x228))

    def testNeutral_ParseNeutral(self):
        val = self.c.parseValue(hexmsg("228 00 00 00 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testNeutral_ParseNotNeutral(self):
        val = self.c.parseValue(hexmsg("228 00 04 00 00 00 00 00 00"))
        self.assertEqual(0x04, val)

    def testNeutral_ParseNeutralWhenOtherByteSet_IgnoresOtherByte(self):
        val = self.c.parseValue(hexmsg("228 00 60 00 00 00 00 00 00"))
        self.assertEqual(0x00, val)

    def testNeutral_ParseNotNeutralWhenOtherByteSet_IgnoresOtherByte(self):
        val = self.c.parseValue(hexmsg("228 00 64 00 00 00 00 00 00"))
        self.assertEqual(0x04, val)

    def testNeutral_CorrectedValue_InNeutral(self):
        self.assertEqual(1, self.c.getCorrectedValue(0x00))

    def testNeutral_CorrectedValue_NotInNeutral(self):
        self.assertEqual(0, self.c.getCorrectedValue(0x04))

    def testNeutral_CorrectedValue_NotSet(self):
        self.assertEqual(None, self.c.getCorrectedValue(None))

    def testNeutral_CorrectedValue_UnknownValue(self):
        self.assertEqual(None, self.c.getCorrectedValue(0x28))


class ControlTester(unittest.TestCase):

    def assertSender(self, sender):
        self.assertEqual(sender, self.c.controlDef.sender)

    def assertValue(self, value, msg):
        self.assertEquals(value, self.c.parseValue(hexmsg(msg)))

    def assertCorrectedValue(self, correctedValue, rawValue):
        self.assertEqual(correctedValue, self.c.getCorrectedValue(rawValue))


class ReverseTest(ControlTester):

    def setUp(self):
        self.c = Control(CONTROL_DEFS['reverse'])

    def testReverse(self):
        self.assertSender(0x39E)

        self.assertValue(0x00, "39E 00 00 00 00 00 00 00 00")
        self.assertValue(0x10, "39E 00 00 00 10 00 00 00 00")
        self.assertValue(0x10, "39E 00 00 00 16 00 00 00 00")
        self.assertValue(0x00, "39E 00 00 00 06 00 00 00 00")

        self.assertCorrectedValue(1, 0x10)
        self.assertCorrectedValue(0, 0x00)
        self.assertCorrectedValue(None, 0x66)
        self.assertCorrectedValue(None, None)

class ClutchTest(ControlTester):

    def setUp(self):
        self.c = Control(CONTROL_DEFS['clutch'])

    def testClutch(self):
        self.assertSender(0x050)

        self.assertValue(0x00, "050 00 00 00 00 00 00 00 00") #zero
        self.assertValue(0x01, "050 00 00 00 01 00 00 00 00") #clutch out
        self.assertValue(0x02, "050 00 00 00 02 00 00 00 00") #clutch in
        self.assertValue(0x01, "050 00 00 00 21 00 00 00 00") #other value + clutch out

        self.assertCorrectedValue(0, 0x00) #no data
        self.assertCorrectedValue(0, 0x01) #clutch out
        self.assertCorrectedValue(1, 0x02) #clutch in
        self.assertCorrectedValue(None, 0x66) #unhandled data
        self.assertCorrectedValue(None, None) #null data

"""Steering wheel data comes from 0x082. There are 2 readings,
bytes (6,5) and bytes (4,3) which differ slightly. The data is
big endian and read straight from the message. The hex value is 10x
the number of degrees off center (0 deg).

>0 is turning the wheel to the right
To the left, it wraps to 65535 and counts down.

So, TDC is 0/65535. One revolution left (-360 deg) is ~(65535-3600).
One revolution right (+360 deg) is ~3600
"""


class SteeringWheel1Test(ControlTester):

    def setUp(self):
        self.c = Control(CONTROL_DEFS['steering1'])

    def testSteeringWheel1(self):
        self.assertSender(0x082)

        self.assertValue(0x0000, "082 00 FC 00 00 00 00 00 00") # 0s, no data
        self.assertValue(0xEB2E, "082 64 FC EB 2E EA B6 FF B0") # ?? deg : Chock left
        self.assertValue(0xF1F0, "082 58 FC F1 F0 F1 78 00 14") # -360 deg
        self.assertValue(0x000A, "082 4B FC 00 0A FF 92 00 00") # 0 deg : Top Dead Center (TDC)
        self.assertValue(0x0E24, "082 4C FC 0E 24 0D AC FF EC") # +360 deg
        self.assertValue(0x14B4, "082 78 FC 14 B4 14 3C 00 00") # ?? deg : Chock right

        self.assertCorrectedValue(-533, 0xEB2E) #Chock left
        self.assertCorrectedValue(-360, 0xF1F0) #-360 deg
        self.assertCorrectedValue(0, 0x0000) #0 deg, TDC
        self.assertCorrectedValue(362, 0x0E24) #+360 deg
        self.assertCorrectedValue(530, 0x14B4) #Chock right

        self.assertCorrectedValue(0, 0x00) #No data
        self.assertCorrectedValue(None, None) #No data


if __name__ == '__main__':
    unittest.main()
