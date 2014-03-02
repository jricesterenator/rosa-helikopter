#__author__ = 'jjrice'
#
#import unittest
#from quadcopter.car.controls import *
#from quadcopter.car.car import parseCANString
#
#def hexmsg(hexString):
#    sender, hexmsg = parseCANString(hexString)
#    return hexmsg
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
#class GenericControlsTest(unittest.TestCase):
#
#    def setUp(self):
#        self.c = CANControl("Custom Control", sender=0xA3, byteIndex=3, mask=0xFF, cvfunc=lambda x:2*x)
#
#    def testControl_SenderMatches(self):
#        self.assertTrue(self.c._sender_matches(0xA3))
#
#    def testControl_SenderDoesntMatch(self):
#        self.assertFalse(self.c._sender_matches(0x205))
#
#    def testControl_ParseOff(self):
#        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 00 00 00"))
#        self.assertEqual(0x00, val)
#
#    def testControl_ParseOn(self):
#        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 20 00 00"))
#        self.assertEqual(0x20, val)
#
#    def testControl_ParseOnWhenOtherByteSet_PermissiveMask(self):
#        self.c.mask = 0xFF
#        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 28 00 00"))
#        self.assertEqual(0x28, val)
#
#    def testControl_ParseOnWhenOtherByteSet_RestrictiveMask(self):
#        self.c.mask = 0xF0
#        val = self.c.parseValue(hexmsg("0A3 00 00 00 00 00 28 00 00"))
#        self.assertEqual(0x20, val)
#
#    def testControl_CorrectedValue_Off(self):
#        self.assertEqual(0, self.c.getCorrectedValue(0x00))
#
#    def testControl_CorrectedValue_On(self):
#        self.assertEqual(2*0x20, self.c.getCorrectedValue(0x20))
#
#    def testControl_CorrectedValue_NotSet(self):
#        self.assertEqual(None, self.c.getCorrectedValue(None))
#
#    def testControl_CorrectedValue_UnknownValue(self):
#        #Pretend that getCorrectedValue returns a ValueError because it can't translate the value
#        def raiseError(value):
#            raise ValueError
#
#        self.controlDef.correctionFx = raiseError
#        self.assertEqual(None, self.c.getCorrectedValue(0x28))
#
#    def testControl_ListenersCalled(self):
#        la1 = ListenerAssertion(self)
#        la2 = ListenerAssertion(self)
#        self.c.listeners = [la1.onListener, la2.onListener]
#
#        #Test value changing from NOT_SET to 0x20
#        la1.name = "Custom Control"
#        la1.prevValue = None
#        la1.value = 0x20
#
#        la2.name = "Custom Control"
#        la2.prevValue = None
#        la2.value = 0x20
#
#        self.c.onControlChange(0x20)
#        self.assertTrue(la1.wasCalled)
#        self.assertTrue(la2.wasCalled)
#
#
#        #Test value changing from 0x20 to 0x00
#        la1.wasCalled = False
#        la1.prevValue = 0x20
#        la1.value = 0x00
#
#        la2.wasCalled = False
#        la2.prevValue = 0x20
#        la2.value = 0x00
#
#        self.c.onControlChange(0x00)
#
#        self.assertTrue(la1.wasCalled)
#        self.assertTrue(la2.wasCalled)
#
#if __name__ == '__main__':
#    unittest.main()
