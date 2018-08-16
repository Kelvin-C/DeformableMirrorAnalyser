# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : actions.py
# *
# * Author            : Alice Cao, Kelvin Chan
# *
# * Date created      : 4 Feb 2018
# *
# * Purpose           : Subroutines for circuit data collection.
# *                
# * Subroutines       : 1. Output PWM signal with specified channel number (0-15), duty cycle (0-4095) and frequency (40-1000)
# *                     2. PWM sweep
# *                     3. Time sweep
                        4. Matlab_piezo
# *                     
# * Compatible with   : Adafruit 16-Channel 12-bit PCA9685 PWM/Servo Driver
# *                     Adafruit ADS1115 16-Bit ADC - 4 Channel with Programmable Gain Amplifier
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

from __future__ import division
import numpy as np
import time

# gain scale factors
from gain_lookup import gains

# plotter helper function
from plotter import Plotter

# initialise the hardware
from hardware_init import Adafruit_PWM, AB_PWM, Adafruit_ADC

def go(adapwm, ch, dc):
    """ Generates a PWM with given channel and duty cycles """
    off_tick = int(dc*4095./100.)
    adapwm.set_pwm(ch, 0, off_tick)
    
def go_opposite(adapwm, ch, dc):
    """ Generates a PWM with given channel and duty cycles. The low and high regions are swapped
    when compared with 'go' function. """
    off_tick = int(dc*4095./100.)
    adapwm.set_pwm(ch, off_tick, 0)

class run_adapwm(Adafruit_PWM):
    """ Output a PWM signal on a specified channel (ch: 0-15)
    of a given duty cycle (dc: 0-4095) and
    frequency (fr: 40-1000).
    """
    def __init__(self, ch=0, dc=0, fr=1000):
        self.__ch = ch
        self.__dc = dc

        if fr == None:
            self.__fr = 1000
        else:
            self.__fr = fr
        
        Adafruit_PWM.__init__(self, fr)
        
        self.go()

    def freq(self):
        return self.__fr
        
    def duty_cycle(self):
        return self.__dc
    
    def channel(self):
        return self.__ch
        
    def go(self):
        off_tick = int(self.duty_cycle()*4095./100.)
        self.adapwm().set_pwm(self.channel(), 0, off_tick)


class pwm_sweep(Adafruit_ADC):
    """ Perform a sweep over N different values of duty cycles and record output voltage from the ADC.
    Specify a file name,
    number of trials,
    gain value (please refer to gain_lookup.py) and
    whether a reference volage was used (optional).

    Outputs two files:
    1. "means" file with voltage data averaged over all trials, along with standard deviation values.
    2. "raw" with all collected data.

    Graph of "means" data is plotted using Plotter class imported from plotter.py.
    """
    def __init__(self, filename="", N=0, trials=1, g=0, ref=None):
        self.__filename=filename
        self.__N = N
        self.__trials = int(trials)
        self.__gain = g
        self.__ref = ref
        
        Adafruit_ADC.__init__(self, g)
        
        self.sweep()

    def N(self):
        return self.__N

    def name(self):
        if self.__filename == "":
            nme= "pwm_sweep_N=" + str(self.__N)+ "_"+time.strftime("%d_%m_%H%M")
            return str(nme) + ".txt"
        else:
            return str(self.__filename) + ".txt"
    
    def gain(self):
        return self.__gain

    def reference(self):
        return str(self.__ref)
        
    def duty_cycles(self):
        dc = np.linspace(0,100,self.__N)
        return dc

    def sweep(self):
        g=self.gain()
        max_voltage = float(gains[str(g)])
        scale_fac = max_voltage/2**15
        samples = self.duty_cycles()

        data_array = np.zeros([self.__trials, self.N()])
        grounds_array = np.zeros([self.__trials, self.N()])
        references_array = np.zeros([self.__trials, self.N()])
        
        print("collectiing data...")
        print('|trial| point | V | GND | REF |'.format(*range(3)))
        print('-' * 37)

        for i in range(self.__trials):
            run_adapwm(0, 0)
            time.sleep(3)
            for j in range(len(samples)):
                run_adapwm(0, samples[j])
                time.sleep(2)
                # Data pin: A0, ground pin: A1, reference voltage pin: A2.
                data_array[i][j] = self.adaadc().read_adc(0, gain=g, data_rate=8)*scale_fac
                grounds_array[i][j] = self.adaadc().read_adc(1, gain=g, data_rate=8)
                references_array[i][j] = self.adaadc().read_adc(2, gain=g, data_rate=8)
                print(str(i) + " " + str(j)+"\t" + str(data_array[i][j]) + "\t" + str(grounds_array[i][j]) + "\t" + str(references_array[i][j]) +"\n")
        print("Finished collectiing data")
        
        mean_ref = references_array.mean()*scale_fac

        if "%.3f" %  mean_ref== self.reference():
            print("The ADC measured the reference voltage as " + self.reference() + ", as expected.")

        else:
            print("The mean reference voltage measured by the ADC was " + str(references_array.mean()*scale_fac) + ", but expected " + self.reference())

        means = np.zeros(self.N())
        stds = np.zeros(self.N())

        for k in range(self.N()):
            means[k] = data_array.T[k].mean()
            stds[k] = data_array.T[k].std()

        # writing the files!
        off_tick_scale_fac = 4095./100.
        mean_file = open("means_" + self.name(), "w")
        mean_file.write("Duty cycle off_tick" + "\tmean_voltage[V]" + "\tstd dev[V]" + "\tINFO: gain="+str(max_voltage) + "\treference=" + self.reference() + "\ttrials="+str(self.__trials)+"\n")
        for l in range(self.N()):
            mean_file.write(str(samples[l]*off_tick_scale_fac) + "\t" + str(means[l]) + "\t" + str(stds[l]) + "\n")
        mean_file.close()

        raw_file = open("raw_"+self.name(), "w")
        raw_file.write("\nraw_voltage_data\n")
        for m in data_array:
            for mi in range(m.size):
                raw_file.write(str(m[mi]) + " ")
            raw_file.write("\n")

        raw_file.write("\nraw_ground_pin_data\n")
        for n in grounds_array:
            for ni in range(n.size):
                raw_file.write(str(n[ni]) + " ")
            raw_file.write("\n")

        raw_file.write("\nraw_ref_voltage_data\n")
        for o in references_array:
            for oi in range(o.size):
                raw_file.write(str(o[oi]) + " ")
            raw_file.write("\n")
            
        Plotter("means_"+self.name()).stat_plot(title="PWM sweep", x_axis="PWM off tick", y_axis="Voltage [V]")

class time_sweep(Adafruit_ADC):   
    """ Perform a time sweep. Switches on the PWM board at a given duty cycle value and starts recording ADC voltage data.
    Specify the duration, t, of the sweep at which the PWM board is switched off. Data continues to be recorded for 4 seconds after switchoff time.

    Outputs one file:
    1. "time_sweep" data

    Graph of data is plotted using Plotter class imported from plotter.py.
    """
    def __init__(self, t=0, dc=50, gain=1, fn=None, ch=None, dr=None):
        self.__filename=fn
        self.__t=t
        self.__dc = dc
        self.__ch = ch
        self.__dr = dr
       
        Adafruit_ADC.__init__(self, gain)
       
        self.t_sweep()

    def name(self):
        if self.__filename == None:
            nme= "time_sweep_"+time.strftime("%d_%m_%H%M")
            return nme+".txt"
        else:
            return self.__filename + ".txt"

    def data_rate(self):
        if self.__dr == None:
            return 860
        else:
            return self.__dr
   
    def time(self):
        return self.__t

    def duty_cycle(self):
        return self.__dc

    def channel(self):
        if self.__ch == None:
            return int(0)
        else:
            return int(self.__channel)
       
    def t_sweep(self):
        t = self.time()
        g=self.gain()
        max_voltage = float(gains[str(g)])
        data_pts = []
        time_pts = []
        ch = self.channel()
        dc= self.duty_cycle()
        
        run_adapwm(self.channel(), 0)
        time.sleep(1)

        start_time = time.time()
        
        run_adapwm(ch, dc)
        while time.time()-start_time < t:
            data_pts.append(self.adaadc().read_adc(0, gain=g))
            time_pts.append(time.time())

        discharge_t = time.time()

        run_adapwm(self.channel(), 0)
        while time.time() - discharge_t < 4:
            data_pts.append(self.adaadc().read_adc(0, gain=g))
            time_pts.append(time.time())
        
        max_voltage = float(gains[str(g)])
            
        voltages = np.array(data_pts)*max_voltage/2**15
        times = np.array(time_pts) - start_time

        file = open(str(self.name()), "w")
        file.write("Time [s] \t Voltage \t Gain=" + str(max_voltage) + "\n")

        for i in range(voltages.size): 
            file.write(str(times[i]) + "\t" + str(voltages[i])+"\n")

        file.close()
        
        Plotter(self.name()).show_plot(title="time sweep", x_axis="time [s]", y_axis="Voltage [V]")

class Matlab_piezo():
    """ Performs a change in stroke for the connected piezoelectric actuators given:

    adapwm: the variable which controls the PWM.
    ch: list of channels that the PWM connects to the piezo actuators.
    dc: list of duty cycles corresponding to the actuators.
    connection: The variable which states whether a connection with the MATLAB computer is connected.
    fr: frequency of PWM.

    Outputs the given duty cycles to the given channels.
    """

    def __init__(self, adapwm, ch, dc, connection, fr=1000):
        self.__adapwm = adapwm
        self.__fr = fr
        self.__dc = dc
        self.__ch = ch
        self.__connection = connection

        self.run_pwm()

    def adapwm(self):
        return self.__adapwm

    def freq(self):
        return self.__fr

    def dutycycle(self):
        return self.__dc

    def channels(self):
        return self.__ch

    def num_of_piezos(self):
        return len(self.channels())

    def change_dutycycle(self, new_dc):
        self.__dc = new_dc

    def connection(self):
        return self.__connection

    def run_pwm(self):
        ch = self.channels()
        dc = self.dutycycle()
        adapwm = self.adapwm()

        for i in range(self.num_of_piezos()):
            go(adapwm, ch[i], dc[i])
        if self.connection() != False:
            self.connection().send("Finished")