#
# Use this script to create a software serial connection between 2 mock
# devices.
#
# This useful for integration testing when it's not possible to connect to the
# real car. The quadcopter program can connect to a mock car (can_simulator.py)
# over serial. The mock car pumps mock CAN messages over the serial link.
#
# Usage:
#   1. Run this to setup the serial link.
#   2. Start the mock car/CAN simulator (can_simulator.py)
#   3. Start the quadcopter program.
#   4. Use the CAN simulator to pump commands or manually send them one-by-one
#
socat PTY,link=/tmp/fake1,raw,echo=0 PTY,link=/tmp/fake2,raw,echo=0
