# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : server.py
# *
# * Author            : Alice Cao and Kelvin Chan
# *
# * Date created      : 10 MAR 2018
# *
# * Purpose           : Allow the Raspberry Pi to accept values sent from another computer to control duty cycles.
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

import socket
import numpy as np
import Adafruit_PCA9685
import actions

pwm = Adafruit_PCA9685.PCA9685()

#IP Address of the Raspberry Pi
host = "169.254.99.105"
port = 30004

print(host)
print(port)

#Setting up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)

while True:
    #Accept the data sent by MATLAB
    c, addr = s.accept()
    msg = c.recv(64)
    if len(msg) >0:
        #Read the data sent by MATLAB and convert them into duty cycles.
        pwm_array = np.array(msg[1:-1].split())
        pwm_array = map(float, pwm_array)
        print(pwm_array)

        #Output the duty cycles to the deformable mirror.
        actions.Matlab_piezo(adapwm=pwm, ch=[0,1,2], dc=pwm_array, connection=c, fr=1000)

        c.send("1")
        c.close()