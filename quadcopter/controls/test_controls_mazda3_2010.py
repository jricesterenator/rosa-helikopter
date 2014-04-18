#__author__ = 'jjrice'
#
import unittest
from mazda3_2010 import MAZDA_3_2010_CAN_CONTROLS
from quadcopter.car.car import parseCANString, parseCANValue
#
def hexmsg(hexString):
    sender, hexmsg = parseCANString(hexString)
    return sender, hexmsg
#
#class ListenerAssertion:
#
#    def __init__(self, testClass):
#        self.wasCalled = False
#        self.testClass = testClass
#
#    def onListener(self, control):
#        self.wasCalled = True
#
#        self.testClass.assertEqual(self.name, control.name)
#        self.testClass.assertEqual(self.prevValue, control.prevValue)
#        self.testClass.assertEqual(self.value, control.value)
#
class HandbrakeTest(unittest.TestCase):

    def testBrake(self):
        self.c = MAZDA_3_2010_CAN_CONTROLS['hazards']
        self.assertTrue(self.c.senderMatches(0x39E))

        sender, hexMsg = parseCANString("39E 00 03 20 7F 00 10 01 0E")
        value = parseCANValue(hexMsg, self.c.byteIndex, self.c.mask)
        print "Value:", hex(value)


    #class ControlTester(unittest.TestCase):
#
#    def assertSender(self, sender):
#        self.assertEqual(sender, self.c.sender)
#
#    def assertValue(self, value, msg):
#        self.assertEquals(value, parseCANValue(hexmsg(msg)))
#
#    def assertCorrectedValue(self, correctedValue, rawValue):
#        self.assertEqual(correctedValue, self.c._getCorrectedValue(rawValue))
#
#class BrakeTest(unittest.TestCase):
#
#    def setUp(self):
#        self.c = MAZDA_3_2010_CONTROLS['brake']
#
#    def testBrake_SenderMatches(self):
#        self.assertTrue(self.c._senderMatches(0x190))
#
#    def testBrake_ParseBrakeNotActive(self):
#        val = parseCANValue(hexmsg("190 00 00 00 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testBrake_ParseBrakeActive(self):
#        val = parseCANValue(hexmsg("190 00 00 40 00 00 00 00 00"))
#        self.assertEqual(0x40, val)
#
#    def testBrake_ParseBrakeActiveWhenOtherByteSet_IgnoresOtherByte(self):
#        val = parseCANValue(hexmsg("190 00 00 46 00 00 00 00 00"))
#        self.assertEqual(0x40, val)
#
#    def testBrake_ParseBrakeNotActiveWhenOtherByteSet_IgnoresOtherByte(self):
#        val = parseCANValue(hexmsg("190 00 00 06 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testBrake_CorrectedValue_BrakeActive(self):
#        self.assertEqual(1, self.c._getCorrectedValue(0x40))
#
#    def testBrake_CorrectedValue_BrakeNotActive(self):
#        self.assertEqual(0, self.c._getCorrectedValue(0x00))
#
#    def testBrake_CorrectedValue_NotSet(self):
#        self.assertEqual(None, self.c._getCorrectedValue(None))
#
#    def testBrake_CorrectedValue_UnknownValue(self):
#        self.assertEqual(None, self.c._getCorrectedValue(0x28))
#
#class HandbrakeTest(unittest.TestCase):
#
#    def setUp(self):
#        self.c = MAZDA_3_2010_CONTROLS['handbrake']
#
#    def testHandbrake_SenderMatches(self):
#        self.assertTrue(self.c._senderMatches(0x39E))
#
#    def testHandbrake_ParseOff(self):
#        val = parseCANValue(hexmsg("39E 00 00 00 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testHandbrake_ParseOn(self):
#        val = parseCANValue(hexmsg("39E 00 00 20 00 00 00 00 00"))
#        self.assertEqual(0x20, val)
#
#    def testHandbrake_ParseOnWhenOtherByteSet_IgnoresOtherByte(self):
#        val = parseCANValue(hexmsg("39E 00 00 28 00 00 00 00 00"))
#        self.assertEqual(0x20, val)
#
#    def testHandbrake_CorrectedValue_Off(self):
#        self.assertEqual(0, self.c._getCorrectedValue(0x00))
#
#    def testHandbrake_CorrectedValue_On(self):
#        self.assertEqual(1, self.c._getCorrectedValue(0x20))
#
#    def testHandbrake_CorrectedValue_NotSet(self):
#        self.assertEqual(None, self.c._getCorrectedValue(None))
#
#    def testHandbrake_CorrectedValue_UnknownValue(self):
#        self.assertEqual(None, self.c._getCorrectedValue(0x28))
#
#class InGearTest(unittest.TestCase):
#
#    def setUp(self):
#        self.c = MAZDA_3_2010_CONTROLS['ingear']
#
#    def testInGear_SenderMatches(self):
#        self.assertTrue(self.c._senderMatches(0x228))
#
#    def testInGear_ParseNotInGear(self):
#        val = parseCANValue(hexmsg("228 00 00 00 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testInGear_ParseInGear(self):
#        val = parseCANValue(hexmsg("228 00 04 00 00 00 00 00 00"))
#        self.assertEqual(0x04, val)
#
#    def testInGear_ParseInGearWhenOtherByteSet_IgnoresOtherByte(self):
#        val = parseCANValue(hexmsg("228 00 64 00 00 00 00 00 00"))
#        self.assertEqual(0x04, val)
#
#    def testInGear_ParseNotInGearWhenOtherByteSet_IgnoresOtherByte(self):
#        val = parseCANValue(hexmsg("228 00 60 00 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testInGear_CorrectedValue_InGear(self):
#        self.assertEqual(1, self.c._getCorrectedValue(0x04))
#
#    def testInGear_CorrectedValue_NotInInGear(self):
#        self.assertEqual(0, self.c._getCorrectedValue(0x00))
#
#    def testInGear_CorrectedValue_NotSet(self):
#        self.assertEqual(None, self.c._getCorrectedValue(None))
#
#    def testInGear_CorrectedValue_UnknownValue(self):
#        self.assertEqual(None, self.c._getCorrectedValue(0x28))
#
#class NeutralTest(unittest.TestCase):
#
#    def setUp(self):
#        self.c = MAZDA_3_2010_CONTROLS['neutral']
#
#    def testNeutral_SenderMatches(self):
#        self.assertTrue(self.c._senderMatches(0x228))
#
#    def testNeutral_ParseNeutral(self):
#        val = parseCANValue(hexmsg("228 00 00 00 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testNeutral_ParseNotNeutral(self):
#        val = parseCANValue(hexmsg("228 00 04 00 00 00 00 00 00"))
#        self.assertEqual(0x04, val)
#
#    def testNeutral_ParseNeutralWhenOtherByteSet_IgnoresOtherByte(self):
#        val = parseCANValue(hexmsg("228 00 60 00 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testNeutral_ParseNotNeutralWhenOtherByteSet_IgnoresOtherByte(self):
#        val = parseCANValue(hexmsg("228 00 64 00 00 00 00 00 00"))
#        self.assertEqual(0x04, val)
#
#    def testNeutral_CorrectedValue_InNeutral(self):
#        self.assertEqual(1, self.c._getCorrectedValue(0x00))
#
#    def testNeutral_CorrectedValue_NotInNeutral(self):
#        self.assertEqual(0, self.c._getCorrectedValue(0x04))
#
#    def testNeutral_CorrectedValue_NotSet(self):
#        self.assertEqual(None, self.c._getCorrectedValue(None))
#
#    def testNeutral_CorrectedValue_UnknownValue(self):
#        self.assertEqual(None, self.c._getCorrectedValue(0x28))
#
#class ReverseTest(ControlTester):
#
#    def setUp(self):
#        self.c = MAZDA_3_2010_CONTROLS['reverse']
#
#    def testReverse(self):
#        self.assertSender(0x39E)
#
#        self.assertValue(0x00, "39E 00 00 00 00 00 00 00 00")
#        self.assertValue(0x10, "39E 00 00 00 10 00 00 00 00")
#        self.assertValue(0x10, "39E 00 00 00 16 00 00 00 00")
#        self.assertValue(0x00, "39E 00 00 00 06 00 00 00 00")
#
#        self.assertCorrectedValue(1, 0x10)
#        self.assertCorrectedValue(0, 0x00)
#        self.assertCorrectedValue(None, 0x66)
#        self.assertCorrectedValue(None, None)
#
#class ClutchTest(ControlTester):
#
#    def setUp(self):
#        self.c = MAZDA_3_2010_CONTROLS['clutch']
#
#    def testClutch(self):
#        self.assertSender(0x050)
#
#        self.assertValue(0x00, "050 00 00 00 00 00 00 00 00") #zero
#        self.assertValue(0x01, "050 00 00 00 01 00 00 00 00") #clutch out
#        self.assertValue(0x02, "050 00 00 00 02 00 00 00 00") #clutch in
#        self.assertValue(0x01, "050 00 00 00 21 00 00 00 00") #other value + clutch out
#
#        self.assertCorrectedValue(0, 0x00) #no data
#        self.assertCorrectedValue(0, 0x01) #clutch out
#        self.assertCorrectedValue(1, 0x02) #clutch in
#        self.assertCorrectedValue(None, 0x66) #unhandled data
#        self.assertCorrectedValue(None, None) #null data
#
#"""Steering wheel data comes from 0x082. There are 2 readings,
#bytes (6,5) and bytes (4,3) which differ slightly. The data is
#big endian and read straight from the message. The hex value is 10x
#the number of degrees off center (0 deg).
#
#>0 is turning the wheel to the right
#To the left, it wraps to 65535 and counts down.
#
#So, TDC is 0/65535. One revolution left (-360 deg) is ~(65535-3600).
#One revolution right (+360 deg) is ~3600
#"""
#class SteeringWheel1Test(ControlTester):
#
#    def setUp(self):
#        self.c = MAZDA_3_2010_CONTROLS['steering1']
#
#    def testSteeringWheel1(self):
#        self.assertSender(0x082)
#
#        self.assertValue(0x0000, "082 00 FC 00 00 00 00 00 00") # 0s, no data
#        self.assertValue(0xEB2E, "082 64 FC EB 2E EA B6 FF B0") # ?? deg : Chock left
#        self.assertValue(0xF1F0, "082 58 FC F1 F0 F1 78 00 14") # -360 deg
#        self.assertValue(0x000A, "082 4B FC 00 0A FF 92 00 00") # 0 deg : Top Dead Center (TDC)
#        self.assertValue(0x0E24, "082 4C FC 0E 24 0D AC FF EC") # +360 deg
#        self.assertValue(0x14B4, "082 78 FC 14 B4 14 3C 00 00") # ?? deg : Chock right
#
#        self.assertCorrectedValue(-533, 0xEB2E) #Chock left
#        self.assertCorrectedValue(-360, 0xF1F0) #-360 deg
#        self.assertCorrectedValue(0, 0x0000) #0 deg, TDC
#        self.assertCorrectedValue(362, 0x0E24) #+360 deg
#        self.assertCorrectedValue(530, 0x14B4) #Chock right
#
#        self.assertCorrectedValue(0, 0x00) #No data
#        self.assertCorrectedValue(None, None) #No data
#
#
if __name__ == '__main__':
    unittest.main()
