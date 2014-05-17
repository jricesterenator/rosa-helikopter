OBD-II Documentation Reference
==============================

AT-commands-cheat-sheet.pdf
---------------------------
Quick reference of the AT commands used to interact with the OBD-II dongle.
Should be supported by all ELM 327 dongles.

ELM327DS.pdf
------------
Full datasheet about the ELM327 chip for communicating over OBD-II. Has full
command list, descriptions, and usage examples.

STN1100-frpm.pdf
----------------
Datasheet and programming manual for the STN chip for communicating over OBD-II.
The STN chip is a superset of the ELM chip, providing it's own ST commands. It
has more features and better performance than an ELM. It is fully compatible
with the AT commands. (The STN can setup complex filters about which CAN events
to process/not process, and it can switch between the HS and MS CAN busses on
the fly.)

stn1110_vs_elm327.pdf
---------------------
At-a-glance comparison of the ELM vs STN chips.

mx_protocol_commands.pdf
------------------------
Good list of the different busses vehicles can support. Use this information to switch between HS and MS CAN busses.

mynotes.rtf
-----------
All my notes about decoding the 2010 Mazda 3 high speed and medium speed CAN bus
messages.
