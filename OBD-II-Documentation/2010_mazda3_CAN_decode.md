#JRTODO: what's this?
3944409762ex
file://localhost/Users/jjrice/Desktop/mazdatechinfo/manual/books/i3w09/html/id0902g9960700.html

#JRTODO: show example messages for each


##### 050 - Clutch
```
  Byte 5 - Clutch in/out
    01 (0000 0001) - Out
    02 (0000 0010) - In
```

##### 082 - Steering wheel position
```  
  Byte 1/2 - Seems to be related to the electronic steering assist motor. When you hear it whirring, these values appear. When it stops, these go to 0000.
```
```
  Byte 3/4 - Steering wheel position1 (slightly off from bytes 5/6. Maybe there are 2 sensors?)
    (See bytes 5/6 for more info)
    Max CW rotation is ~530 deg; Max CCW rotation is ~ -530 deg
    Example:
      082 5A FC FC EB EA C0 00 00 (Chock left)
      082 5A FC 14 B4 01 40 00 00 (Chock right)
                      ^^^^^
      Words            : Chock Left .... TDC     ....Chock Right
      Hex              : EAC0       .... FFFF/0  ....3C00
      Decimal          : 60096      .... 65535/0 ....5180
      10ths of a degree: -5440      .... 0       ....5180
      Degrees          : -544       .... 0       ....518      
```
```
  Byte 5/6 - Steering wheel position2 (slightly off from bytes 3/4. Maybe there are 2 sensors?)
    Steering wheel position is a 2 byte Big Endian value expressed in 10ths of a degree.
    Top dead center (TDC) is 0 (00 00)
    CW rotation is > 0 (> 00 00)
    CCW rotation is <= 65535 (<= FF FF)...Note that 65535 is actually -1/10th of a degree; likewise 65526 is -1 degree.
    Max CW rotation is ~530 deg; Max CCW rotation is ~ -530 deg
    082 5A FC FC EB 01 40 00 00 (Chock left)
    082 5A FC 14 B4 01 40 00 00 (Chock right)
              ^^^^^
    Example:
      Words            : Chock Left .... TDC     ....Chock Right
      Hex              : FCEB       .... FFFF/0  ....14B4
      Decimal          : 60216      .... 65535/0 ....5300
      10ths of a degree: -5320      .... 0       ....5300
      Degrees          : -532       .... 0       ....530
```
```
  Byte 7 - Always FC
    FC = ??
  Byte 8 - Counter (rolls around so you know the sequence of messages. First digit can be different when you start the car different times. Second digit goes 0,1,2..F,0,1..F...)
```

165 - Engine speed, accel pedal
  Byte 4 - Accel pedal (2 discrete vals). Useful to see if the pedal is activated, but when you don't care it's exact value.
    C0 = Pedal is completele up
    00 = Any amount of activation.


170 - Another accelerator pedal position
  170 26 EE 27 99 27 1C 6B 17 (Up)
  170 26 EE 27 99 28 CB 6A 17 (Down)
  Bytes 3/4: Accelerator pedal (range)
    27 1C = Up
    28 CB = Down
    
190 - Brake
  190 00 00 00 00 00 00 00 00 (Not depressed)
  190 00 00 40 00 00 00 00 00 (Depressed)
  Byte 6
    00 (0000 0000) = Not depressed
    40 (0100 0000) = Depressed


200 - RPM-based

201 - RPM-based; Accel pedal
  Byte 2 - Accelerator pedal (2 bytes, range)
    00 = Up
    ...
    C8 = Fully depressed

205 - Brake (JRTODO: verify!)
  205 00 00 40 00 00 00 00 00 
  Byte 6 - Brake
    00 (0000 0000) = Up
    40 (0100 0000) = Depressed

20F - ???

211 - DSC, ??
  Byte 3 - DSC button (stability control)
    00 (0000 0000) = Off
    48 (0100 1000) = On
    
212 - ???
    
228 - Neutral indicator
  228 00 00 00 00 00 00 00 00 (neutral)
  228 00 04 00 00 00 00 00 00 (in gear)
  Byte 7 - Neutral/In gear indicator.
    0x00 = Neutral
    0x04 = In gear (JRTODO: does this include reverse??)
  Other bytes:
    00 - All 0s

231 - ???

240 - ???
    
250 - RPM-based; Accelerator pedal
  250 00 30 94 26 36 14 00 04 (Up)
  250 00 30 94 D7 36 D2 00 04 (Fully down)
  Bytes ?? Unclear. 3-6? or 4-5 or 3? (JRTODO)

274 - Clutch??? (JRTODO)

340 - ???

350 - ???

37B - ???

39E - Steering wheel sticks ops
  Default State: 39E 00 00 00 7F 00 10 01 17
#JRTODO what's this? file://localhost/Users/jjrice/Desktop/mazdatechinfo/manual/books/i3w09/html/id0902f5960700.html
  Byte 1 - ???. Can change, but not sure why.

  Byte 4 - Turn signal activation; Wipers; Reverse
    Signals, stays on while active. (Also see byte 7 which flashes with signal)
    02 (0000 0010) = Right turn signal activated (stays on while active)
    04 (0000 0100) = Left turn signal activated (stays on while active)
    
    Wipers - Pulses between these values when main wiper activated. The transitions between these values isn't always perfect, and sometimes it sticks on a value or spikes to another.
    Low speed: 40..80..40..80
    High speed: 40..C0..40..C0
    #JRTODO: verify when 40 is not wiping or 00 is not wiping. Prev Notes: (80 if triggered, 40 if i spray?)
    00 (0000 0000) = Main wiper off
    40 (0100 0000) = Main wiper active, but not wiping
    80 (1000 0000) = Main wiper wiping action, low speed
    C0 (1100 0000) = Main wiper wiping action, high speed
    
    10 (0001 0000) = Reverse
  
  Byte 6 - Handbrake; lights; defrost
    00 (0000 0000) = Handbrake off; lights off; defrost off
    20 (0010 0000) = Handbrake On
    80 (1000 0000) = Brights only
    08 (0000 1000) = Headlights only (If in auto mode, lights must actually be activated. Can't just be in auto)
    02 (0000 0010) = Rear defrost
 
    Combo examples:
    A0 (1010 0000) = Handbrake + Brights
    88 (1000 1000) = Lights + Brights
    A8 (1010 1000) = Handbrake + Lights + Brights
    
  Byte 7 - Turn signal lights activated, flashes with lights. (Left, Right, Hazards)
    00 (0000 0000) - Right signal light off
    02 (0000 0010) - Right signal light on
    
    00 (0000 0000) - Left signal light off
    01 (0000 0001) - Left signal light on
    
    00 (0000 0000) - Hazard signal lights off
    03 (0000 0011) - Hazard signal lights on
    
  Byte 8 - Door ajar/locked
JRTODO: what does the 2nd part mean? byte 2 "8 to 80 when driver door open, 2 goes to 20 then 10 at the same time; 8 changes with door lock statuses"
  Door Ajar:
    80 (1000 0000) = Driver door open
    40 (0100 0000) = Front passenger door open
    20 (0010 0000) = Rear driver door open
    10 (0001 0000) = Rear passenger door open
    
    Door Locked:
    01 (0000 0001) = Driver door locked (no values for other doors!)

400 - ???

405 - ???

420 - ???

42B - AFS button (JRTODO: verify)
  Byte 8 - AFS button
    00 (0000 0000) = AFS on
    02 (0000 0010) = AFS off

430
(from before:430 21  and 430 22 something to do with seat heating. temp?)
(byte 7)
0011 0111 (default)
0011 0110 (when lights, brights on. Sometimes when rear wiper fluid). Pulse between 36  and 37 when in reverse. or when hazards on. different pulse speed..or when butt heaters on highish

(byte 1) climate fan speed
0000 0000 (off)
0010 0000 (low, 1 click)
0011 0000 (2 clicks)
0100 0000 (3 clicks)
0101 0000 (4 clicks)
0110 0000 (5 clicks)
0111 0000 (6 clicks)
1000 0000 (7 clicks, full)

433 - ???
  (byte 1)
  0000 0000 (no lights)
  0000 0001 (lights on in any fashion)

  Byte 5
  0000 0000 (no handbrake)
  0000 0001 (handbrake)
  0000 0010 (reverse)
  0000 1000 (blower fan on)

461 - Seat belts; Passenger detection
  Byte 7 - Seat belts; Passenger detection
    01 (0000 0001) - No front passenger
    02 (0000 0010) - Front passenger present (enough for airbags at least)
    00 (0000 0000) - No seat belts
    20 (0010 0000) - Driver seatbelt on
    40 (0100 0000) - Front passenger seatbelt on

4B0 - ???

4EC - Cruise
  Byte 8 - Cruise activation
    00 (0000 0000) = Cruise off
    80 (1000 0000) = Cruise on
    C0 (1100 0000) = Cruise active and cruising
 
501 - ???

508 - ???
```
