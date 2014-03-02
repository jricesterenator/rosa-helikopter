from quadcopter.car.controls import *

def steering1(value):
    if value > 60000: #JRTODO: more official way to come up with this number?
        offcenter = value - 65536
    else:
        offcenter = value
    deg = offcenter/10 #convert 10ths of a degree to degree
    return deg

MAZDA_3_2010_CONTROLS = {
    'reverse'  : CANControl('Reverse',   sender=0x39E, byteIndex=5, mask=0xF0, cvmap={0x00:0, 0x10:1}),
    'handbrake': CANControl('Handbrake', sender=0x39E, byteIndex=6, mask=0xF0, cvmap={0x00:0, 0x20:1}),
    'neutral'  : CANControl('Neutral',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:1, 0x04:0}),
    'ingear'   : CANControl('In Gear',   sender=0x228, byteIndex=7, mask=0x0F, cvmap={0x00:0, 0x04:1}),
    'brake'    : CANControl('Brake',     sender=0x190, byteIndex=6, mask=0xF0, cvmap={0x40:1, 0x00:0}),
    'clutch'   : CANControl('Clutch',    sender=0x050, byteIndex=5, mask=0x0F, cvmap={0x00:0, 0x01:0, 0x02:1}),
    'steering1': CANControl('Steering1', sender=0x082, byteIndex=5, mask=0xFFFF, cvfunc=steering1)
}
