## dmUI v.1.0 - 06/06/2018

This Python script generates a UI which allows the user to control piezoelectric actuators with duty cycles.
Any number of actuators can be controlled. A sweeping option is available whereby a range of duty cycles is sent to a particular actuator whilst other actuators remain constant.

### Tested System:
- Windows 10 with 64 bit Python 3.6.4

### Required Python Libraries:
- Instrumental
- Matplotlib
- PIL
- tkinter
- paramiko
- socket

### Variables to edit:
- Change 'ip', 'user' and 'passw' under the function 'login()' to that of the Raspberry Pi.
This allows duty cycles to be sent to the Raspberry Pi.

## How to run:
- Ensure the Raspberry Pi is connected to the computer running this software via Ethernet or Wi-Fi.
- Ensure the IP address and login details are correct (see 'Variables to edit').
- Run 'run.py' and the UI should open.