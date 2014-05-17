from cancar import CANControlDef
from car import SimpleControlDef

"""
    We need to convert to degrees first, then we can set it to -1...1
"""
def steering1_convertToDegrees(value):
    if value > 60000: #JRTODO: more official way to come up with this number?
        offcenter = value - 65536
    else:
        offcenter = value
    deg = offcenter/10 #convert 10ths of a degree to degree
    return deg

def steering1(value):
    degrees = steering1_convertToDegrees(value)

    trim = 5
    max=45

    if -trim <= degrees <= trim:
        return 0

    if degrees >= max:
        return 1

    if degrees <= -max:
        return -1

    return degrees/float(50)

"""
    Pedal position is a continuous value between 0x00 and 0xC8.
"""
def gas1(value):
    return value/float(0xC8)

"""
    These are the inputs I've indentified for the 2010 Mazda for use with the quadcopter.
    I've found more inputs, but haven't listed them here.

    Example from steering column info: 39E 00 00 00 7F 00 10 01 17
    Sender - The sender ID (39E)
    Byte Index - Counted from the right, which pair of bytes to look at?
                 byteIndex=5 points to 0x7F in the example.
    Mask - Mask to apply to the message value to get a final value. Many message values
           use bits as flags and the results is represented in hex.
           Example: Feature 1(bit2) is on; Feature 2(bit3) is off:  0000 0010 (aka 0x02)
           Example: Feature 1(bit2) is on; Feature 2(bit3) is on:   0000 0110 (aka 0x06)
           Example: Feature 1(bit2) is off; Feature 2(bit3) is on:  0000 0100 (aka 0x04)
           Example: Feature 1(bit2) is off; Feature 2(bit3) is off: 0000 0000 (aka 0x00)

    cvmap - A map of CAN values (determined by the mask) to the logical value the program
            should see for this input.
            Example:
            Reverse is sender 39e, byteIndex 4.
            Reverse off - 39E 00 00 00 7F 00 10 01 17
            Reverse on  - 39E 00 00 00 7F 10 10 01 17
                                          ^
            reverse..cvmap={0x00:0, 0x10:1} (If the CAN value is 0x00, the program
            sees 0. If the CAN value is 0x10, the program should see 1). This way, the program
            only has to tell between 0 and 1 to see if reverse is active instead of parsing
            CAN values itself.

    cvfunc - For complex values that aren't a static mapping between CAN value and logical
             value. These need a function to translate.
             For example, steering CAN values
             come as 0 for TDC (top dead center). When you go CCW from there, the value
             wraps to 65536 and decreases. When you go CW, they increase from 0. Additionally,
             the CAN value reports in 10ths of a degrees. So, to get the steering wheel
             position as a range from -1..0..1, we need to calculate which side of 0 and convert
             from 10ths of a degree to whole degrees.
"""
MAZDA_3_2010_CAN_CONTROLS = {
    'reverse'  : CANControlDef('Reverse',   sender=0x39E, byteIndex=4, mask=0x10, cvmap={0x00:0, 0x10:1}),
    'handbrake': CANControlDef('Handbrake', sender=0x39E, byteIndex=6, mask=0x20, cvmap={0x00:0, 0x20:1}),
    'neutral'  : CANControlDef('Neutral',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:1, 0x04:0}),
    'ingear'   : CANControlDef('In Gear',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:0, 0x04:1}),
    'brake'    : CANControlDef('Brake',     sender=0x190, byteIndex=6, mask=0xF0, cvmap={0x40:1, 0x00:0}),
    'clutch'   : CANControlDef('Clutch',    sender=0x050, byteIndex=5, mask=0x0F, cvmap={0x00:0, 0x01:0, 0x02:1}),
    'steering1': CANControlDef('Steering1', sender=0x082, byteIndex=5, mask=0xFFFF, cvfunc=steering1),
    'hazards': CANControlDef('Hazards', sender=0x39E, byteIndex=7, mask=0x03, cvmap={0x03:1, 0x02:0, 0x01:0, 0x00:0}), #need a better way to handle turn signal matches?
    'seatbelt': CANControlDef('Seatbelt', sender=0x461, byteIndex=7, mask=0x20, cvmap={0x20:1, 0x00:0}),
    'highbeams': CANControlDef('High Beams', sender=0x39E, byteIndex=6, mask=0x80, cvmap={0x80:1, 0x00:0}),
    'right_blinker': CANControlDef('Right Blinker', sender=0x39E, byteIndex=4, mask=0x02, cvmap={0x02:1, 0x00:0}),
    'left_blinker': CANControlDef('Left Blinker', sender=0x39E, byteIndex=4, mask=0x04, cvmap={0x04:1, 0x00:0}),
    'gas1': CANControlDef('Gas', sender=0x201, byteIndex=2, mask=0xFF, cvfunc=gas1),
}

"""
    The 'simple' controls used for the 'Simple Car' modes. When testing the
    drone logic, you don't want to manually send the actual CAN commands
    all the time. This lets you easily set the value for the control.

    These should be used with SimpleCar and SimpleConnection.
    Examples:
        reverse,1 - Activate reverse
        reverse,0 - Deactivate reverse
        steering,.3 - Set the steering wheel to .3 of max CW rotation.
"""
MAZDA_3_2010_SIMPLE_CONTROLS = {
    'reverse'   : SimpleControlDef('reverse'),
    'handbrake' : SimpleControlDef('handbrake'),
    'neutral'   : SimpleControlDef('neutral'),
    'ingear'    : SimpleControlDef('ingear'),
    'brake'     : SimpleControlDef('brake'),
    'clutch'    : SimpleControlDef('clutch'),
    'steering1' : SimpleControlDef('steering1'),
    'hazards'   : SimpleControlDef('hazards'),
    'seatbelt'  : SimpleControlDef('seatbelt'),
    'highbeams' : SimpleControlDef('highbeams'),
    'right_blinker'  : SimpleControlDef('right_blinker'),
    'left_blinker'   : SimpleControlDef('left_blinker'),
    'gas1'      : SimpleControlDef('gas1')
}
