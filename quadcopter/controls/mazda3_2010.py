from car.controls import ControlDefs


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


MAZDA_3_2010_CONTROLS = {
    'reverse'  : ControlDefs.CANControlDef('Reverse',   sender=0x39E, byteIndex=4, mask=0x10, cvmap={0x00:0, 0x10:1}),
    'handbrake': ControlDefs.CANControlDef('Handbrake', sender=0x39E, byteIndex=6, mask=0x20, cvmap={0x00:0, 0x20:1}),
    'neutral'  : ControlDefs.CANControlDef('Neutral',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:1, 0x04:0}),
    'ingear'   : ControlDefs.CANControlDef('In Gear',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:0, 0x04:1}),
    'brake'    : ControlDefs.CANControlDef('Brake',     sender=0x190, byteIndex=6, mask=0xF0, cvmap={0x40:1, 0x00:0}),
    'clutch'   : ControlDefs.CANControlDef('Clutch',    sender=0x050, byteIndex=5, mask=0x0F, cvmap={0x00:0, 0x01:0, 0x02:1}),
    'steering1': ControlDefs.CANControlDef('Steering1', sender=0x082, byteIndex=5, mask=0xFFFF, cvfunc=steering1),
    'hazards': ControlDefs.CANControlDef('Hazards', sender=0x39E, byteIndex=7, mask=0x03, cvmap={0x03:1, 0x02:0, 0x01:0, 0x00:0}), #need a better way to handle turn signal matches?
    'seatbelt': ControlDefs.CANControlDef('Seatbelt', sender=0x461, byteIndex=7, mask=0x20, cvmap={0x20:1, 0x00:0}),
    'highbeams': ControlDefs.CANControlDef('High Beams', sender=0x39E, byteIndex=6, mask=0x80, cvmap={0x80:1, 0x00:0}),
    'right_blinker': ControlDefs.CANControlDef('Right Blinker', sender=0x39E, byteIndex=4, mask=0x02, cvmap={0x02:1, 0x00:0}),
    'left_blinker': ControlDefs.CANControlDef('Left Blinker', sender=0x39E, byteIndex=4, mask=0x04, cvmap={0x04:1, 0x00:0}),
    'gas1': ControlDefs.CANControlDef('Gas', sender=0x201, byteIndex=2, mask=0xFF, cvfunc=gas1),
}

MAZDA_3_2010_GENERIC_CONTROLS = {
    'reverse'   : ControlDefs.GenericControlDef('reverse'),
    'handbrake' : ControlDefs.GenericControlDef('handbrake'),
    'neutral'   : ControlDefs.GenericControlDef('neutral'),
    'ingear'    : ControlDefs.GenericControlDef('ingear'),
    'brake'     : ControlDefs.GenericControlDef('brake'),
    'clutch'    : ControlDefs.GenericControlDef('clutch'),
    'steering1' : ControlDefs.GenericControlDef('steering1'),
    'hazards'   : ControlDefs.GenericControlDef('hazards'),
    'seatbelt'  : ControlDefs.GenericControlDef('seatbelt'),
    'highbeams' : ControlDefs.GenericControlDef('highbeams'),
    'right_blinker'  : ControlDefs.GenericControlDef('right_blinker'),
    'left_blinker'   : ControlDefs.GenericControlDef('left_blinker'),
    'gas1'      : ControlDefs.GenericControlDef('gas1')
}
