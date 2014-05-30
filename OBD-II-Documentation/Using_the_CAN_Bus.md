
List Available Serial Ports
===========================

    bash-3.2$ python -m serial.tools.list_ports
    /dev/tty.Bluetooth-Modem
    /dev/tty.Bluetooth-PDA-Sync
    /dev/tty.Nexus4-
    /dev/tty.OBDLinkMX-STN-SPP
    4 ports found
    
    
    
If you're getting a BUFFER FULL error, crank up the baud rate. The problem isthe device is buffering data that the computer isnt pulling out fast enough


USE atcaf0 to get rid of the DATA ERRORs
look at ATS0 for speed improvements
 

ATL1  (turn off \r in line feeds)
ATI (device info)
ATSP0 (verify connected to ECU)


ATSP 6 (CAN 11bit ID, 500kbaud)

ATBRD 08 (set the internal baud rate to 500k)

ATCAF1
>0902
014                      (says 14b total)
0: 49 02 01 4A 4D 31 
1: 42 4C 31 48 35 31 41 
2: 31 32 34 37 32 32 33 

ATCAF0
>0902
NO DATA



ATCAF0
75 26 27 10 00 6C 5C 00 
FF FE 80 00 48 48 00 E7 
27 10 27 10 27 10 27 10 
02 00 0F 01 AA 55 AA 55 

ATCAF1
00 2F 94 27 35 14 00 04 
2: A6 00 00 00 00 00 00 
00 01 14 00 00 00 0B 00 
67 0A F7 08 07 B5 0F FF <DATA ERROR
75 26 27 10 00 5C 6C 00 <DATA ERROR
FF FE 80 00 48 48 00 F6 <DATA ERROR
E: FC FF 4C FE D4 00 00 
7: 10 27 10 27 10 27 10 

ATH1
205 00 00 00 00 00 00 00 00 
228 00 04 00 00 00 00 00 00 
231 01 59 00 00 FF 00 80 00 
240 00 80 00 00 00 00 00 00 
250 00 2F 94 26 35 14 00 04 
090 F7 09 F7 09 07 B6 0F FF <DATA ERROR
20F 75 27 27 10 00 EC DC 00 <DATA ERROR
211 FF FE 80 00 48 48 00 4F <DATA ERROR
082 2F FC FF 4C FE D4 00 00 
4B0 27 10 27 10 27 10 27 10 



ADVANCED FILTERING (see STN1100 datasheet and extended commands)
stfcp (clear all pass filters)
stfap 205,fff (add pass filter for 205)
stfap 228,fff (add pass filter for 228)
stm (monitor using filters)
…the fff's are masks and can be changed to look only at certain bits

