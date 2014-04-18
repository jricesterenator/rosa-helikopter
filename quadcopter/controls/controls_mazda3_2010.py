from car.cancar import CANControlDef
from car.car import SimpleControlDef

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
