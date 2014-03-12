from car.controls import ControlDefs

def steering1(value):
    if value > 60000: #JRTODO: more official way to come up with this number?
        offcenter = value - 65536
    else:
        offcenter = value
    deg = offcenter/10 #convert 10ths of a degree to degree
    return deg

MAZDA_3_2010_CONTROLS = {
    'reverse'  : ControlDefs.CANControlDef('Reverse',   sender=0x39E, byteIndex=4, mask=0xF0, cvmap={0x00:0, 0x10:1}),
    'handbrake': ControlDefs.CANControlDef('Handbrake', sender=0x39E, byteIndex=6, mask=0xF0, cvmap={0x00:0, 0x20:1}),
    'neutral'  : ControlDefs.CANControlDef('Neutral',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:1, 0x04:0}),
    'ingear'   : ControlDefs.CANControlDef('In Gear',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:0, 0x04:1}),
    'brake'    : ControlDefs.CANControlDef('Brake',     sender=0x190, byteIndex=6, mask=0xF0, cvmap={0x40:1, 0x00:0}),
    'clutch'   : ControlDefs.CANControlDef('Clutch',    sender=0x050, byteIndex=5, mask=0x0F, cvmap={0x00:0, 0x01:0, 0x02:1}),
    'steering1': ControlDefs.CANControlDef('Steering1', sender=0x082, byteIndex=5, mask=0xFFFF, cvfunc=steering1),

    #JRTODO: Made-up stuff, set to real values later
    'hazards': ControlDefs.CANControlDef('Hazards', sender=0x998, byteIndex=1, mask=0xFF, cvfunc=lambda x:x),
    'seatbelt': ControlDefs.CANControlDef('Seatbelt', sender=0x999, byteIndex=1, mask=0xFF, cvfunc=lambda x:x),
}

MAZDA_3_2010_GENERIC_CONTROLS = {
    'reverse'   : ControlDefs.GenericControlDef('reverse'),
    'handbrake' : ControlDefs.GenericControlDef('handbrake'),
    'neutral'   : ControlDefs.GenericControlDef('neutral'),
    'ingear'    : ControlDefs.GenericControlDef('ingear'),
    'brake'     : ControlDefs.GenericControlDef('brake'),
    'clutch'    : ControlDefs.GenericControlDef('clutch'),
    'steering1' : ControlDefs.GenericControlDef('steering1'),
    'seatbelt'  : ControlDefs.GenericControlDef('seatbelt'),
    'highbeams' : ControlDefs.GenericControlDef('highbeams'),
    'hazards'   : ControlDefs.GenericControlDef('hazards'),
    'right_blinker'  : ControlDefs.GenericControlDef('right_blinker'),
    'left_blinker'   : ControlDefs.GenericControlDef('left_blinker'),
    'gas1'      : ControlDefs.GenericControlDef('gas1')
}

#JRTODO: reverse is 1 when active, 0 when not. If wipers on it could become 5