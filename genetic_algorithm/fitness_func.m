%  |**********************************************************************;
%  * Project           : MSci Project: PLAS-Smith-3
%  *
%  * Program name      : fitness_func.m
%  *
%  * Author            : Kelvin Chan and Alice Cao
%  *
%  * Date created      : 05 MAR 2018
%  *
%  * Purpose           : The fitness function of the GA. 
%  *                     Sends duty cycles to the Raspberry Pi.
%  *
%  * Revision History  : v1.0
%  *
%  |**********************************************************************;

function y = fitness_func(x)
%Connect to Raspberry Pi with this function
%Change only IP and PORT number
%PORT number is set by the Pi
t = tcpip('169.254.99.105', 30004, 'NetworkRole', 'client');
fopen(t)

%Send the Duty Cycles to Pi
fwrite(t, mat2str(x))

%Add a pause of 1s to ensure actuators get steady-state.
pause(1)

%Read reply from Pi. Pi sends '1' when successful.
reply = fread(t, t.BytesAvailable);
reply = str2num((transpose(char(reply))));

%Confirm the Pi had received the voltages and sent them to the actuators
%Take image and calculate the fitness of the voltages
if reply==1
    y = take_img();
else
    disp("error")
end