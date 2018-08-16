# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : comparison_graphs.py
# *
# * Author            : Alice Cao
# *
# * Date created      : 4 Feb 2018
# *
# * Purpose           : Plots of collected data, run each function to plot the graphs.
# *                 
# * Graphs            : 1. Comparison of PWM sweeps for 8 optoswitches
# *                     2. Comparison of time sweeps for 8 optoswitches, at 50% duty cycle
# *                     3. Comparison of PWM sweeps for 8 optoswitches without deadzone
# *                     4. Switch 2 time sweep comparison
# *                     5. Switch 3 time sweep comparison
# *                     6. Switch 4 time sweep comparison
# *                     7. Switch comparison 1% duty cycle
# *                     8. Switch time sweep comparison 50%, 98% duty cycle
# *                     9. Pi PWM board raw output
# *                     10. Average smoother circuit output, input 3.9V
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

import matplotlib.pyplot as plt
import numpy as np
from plotter import Plotter

def pwm_comparison():
    
    s1_0103=Plotter("switch_data_27_02_2018/s1/pwm_sweep_s1_01mar.txt")
    s1_2602=Plotter("switch_data_27_02_2018/s1/pwm_sweep_s1_26feb.txt")
    s2=Plotter("switch_data_27_02_2018/s2/pwm_sweep_s2.txt")
    s3=Plotter("switch_data_27_02_2018/s3/pwm_sweep_s3_26feb.txt")
    s4=Plotter("switch_data_27_02_2018/s4/pwm_sweep_s4.txt")
    s5=Plotter("switch_data_27_02_2018/s5/pwm_sweep_s5.txt")
    s6=Plotter("switch_data_27_02_2018/s6/pwm_sweep_s6.txt")
    s7=Plotter("switch_data_27_02_2018/s7/pwm_sweep_s7_01mar.txt")
    s8=Plotter("switch_data_27_02_2018/s8/pwm_sweep_s8_01mar.txt")
    
    plt.rcParams.update({'font.size': 20})
    
    plt.title("Comparison of PWM sweeps for 8 optoswitches")
    plt.xlabel("Duty cycle")
    plt.ylabel("Voltage [V]")
    
    plt.plot(s1_0103.x(), s1_0103.y(), label="s1 01Mar")
    plt.plot(s1_2602.x(), s1_2602.y(), label="s1 26Feb")
    plt.plot(s2.x(), s2.y(), label="s2")
    plt.plot(s3.x(), s3.y(), label="s3")
    plt.plot(s4.x(), s4.y(), label="s4")
    plt.plot(s5.x(), s5.y(), label="s5")
    plt.plot(s6.x(), s6.y(), label="s6")
    plt.plot(s7.x(), s7.y(), label="s7")
    plt.plot(s8.x(), s8.y(), label="s8")
    
    plt.legend(loc=4)
    plt.show()

def time_comparison_dc_50():

    s1=Plotter("switch_data_27_02_2018/s1/time_sweep_s1_dc_50_01mar.txt")
    s2=Plotter("switch_data_27_02_2018/s2/time_sweep_s2_dc_50.txt")
    s3=Plotter("switch_data_27_02_2018/s3/time_sweep_s3_dc_50_26feb.txt")
    s4=Plotter("switch_data_27_02_2018/s4/time_sweep_s4_dc_50.txt")
    s5=Plotter("switch_data_27_02_2018/s5/time_sweep_s5_dc_50.txt")
    s6=Plotter("switch_data_27_02_2018/s6/time_sweep_s6_dc_50.txt")
    s7=Plotter("switch_data_27_02_2018/s7/time_sweep_s7_dc_50_01mar.txt")
    s8=Plotter("switch_data_27_02_2018/s8/time_sweep_s8_dc_50_01mar.txt")
    
    plt.title("Comparison of time sweeps for 8 optoswitches, at 50% duty cycle")
    plt.xlabel("Duty cycle")
    plt.ylabel("Voltage [V]")
    
    plt.plot(s1.x(), s1.y(), label="s1 01Mar")
    plt.plot(s2.x(), s2.y(), label="s2")
    plt.plot(s3.x(), s3.y(), label="s3")
    plt.plot(s4.x(), s4.y(), label="s4")
    plt.plot(s5.x(), s5.y(), label="s5")
    plt.plot(s6.x(), s6.y(), label="s6")
    plt.plot(s7.x(), s7.y(), label="s7")
    plt.plot(s8.x(), s8.y(), label="s8")
    
    plt.legend(loc=4)
    plt.show()

def pwm_comparison_no_dz(): #deadzone
    
    s1_0103=Plotter("switch_data_27_02_2018/s1/pwm_sweep_s1_01mar.txt")
    s1_2602=Plotter("switch_data_27_02_2018/s1/pwm_sweep_s1_26feb.txt")
    s2=Plotter("switch_data_27_02_2018/s2/pwm_sweep_s2.txt")
    s3=Plotter("switch_data_27_02_2018/s3/pwm_sweep_s3_26feb.txt")
    s4=Plotter("switch_data_27_02_2018/s4/pwm_sweep_s4.txt")
    s5=Plotter("switch_data_27_02_2018/s5/pwm_sweep_s5.txt")
    s6=Plotter("switch_data_27_02_2018/s6/pwm_sweep_s6.txt")
    s7=Plotter("switch_data_27_02_2018/s7/pwm_sweep_s7_01mar.txt")
    s8=Plotter("switch_data_27_02_2018/s8/pwm_sweep_s8_01mar.txt")
    
    plt.title("Comparison of PWM sweeps for 8 optoswitches without deadzone")
    plt.xlabel("Point no.")
    plt.ylabel("Voltage [V]")

    plt.plot(np.arange(len(s1_0103.y()[10::])), s1_0103.y()[10::], label="s1 01Mar")
    plt.plot(np.arange(len(s1_2602.y()[9::])), s1_2602.y()[9::], label="s1 26Feb")
    plt.plot(np.arange(len(s2.y()[3::])), s2.y()[3::], label="s2")
    plt.plot(np.arange(len(s3.y()[4::])), s3.y()[4::], label="s3")
    plt.plot(np.arange(len(s4.y()[3::])), s4.y()[3::], label="s4")
    plt.plot(np.arange(len(s5.y()[2::])), s5.y()[2::], label="s5")
    plt.plot(np.arange(len(s6.y()[3::])), s6.y()[3::], label="s6")
    plt.plot(np.arange(len(s7.y()[2::])), s7.y()[2::], label="s7")
    plt.plot(np.arange(len(s8.y()[3::])), s8.y()[3::], label="s8")

    plt.legend(loc=4)
    plt.show()

def s2_time_comparison():
    s2dc_1= Plotter("switch_data_27_02_2018/s2/time_sweep_s2_dc_1.txt")
    s2dc_50= Plotter("switch_data_27_02_2018/s2/time_sweep_s2_dc_50.txt")
    s2dc_98= Plotter("switch_data_27_02_2018/s2/time_sweep_s2_dc_98.txt")
    
    plt.title("Switch 2 time sweep comparison")
    plt.xlabel("Duty cycle")
    plt.ylabel("Voltage [V]")
    
    plt.plot(s2dc_1.x(), s2dc_1.y(), label="1")
    plt.plot(s2dc_50.x(), s2dc_50.y(), label="50")
    plt.plot(s2dc_98.x(), s2dc_98.y(), label="98")
    
    plt.legend(loc=1)
    plt.show()

def s3_time_comparison():
    s3dc_1= Plotter("switch_data_27_02_2018/s3/time_sweep_s3_dc_1_26feb.txt")
    s3dc_50= Plotter("switch_data_27_02_2018/s3/time_sweep_s3_dc_50_26feb.txt")
    s3dc_98= Plotter("switch_data_27_02_2018/s3/time_sweep_s3_dc_98_26feb.txt")
    
    plt.title("Switch 3 time sweep comparison")
    plt.xlabel("Duty cycle")
    plt.ylabel("Voltage [V]")
    
    plt.plot(s3dc_1.x(), s3dc_1.y(), label="1")
    plt.plot(s3dc_50.x(), s3dc_50.y(), label="50")
    plt.plot(s3dc_98.x(), s3dc_98.y(), label="98")
    
    plt.legend(loc=1)
    plt.show()

def s4_time_comparison():
    s4dc_1= Plotter("switch_data_27_02_2018/s4/time_sweep_s4_dc_1.txt")
    s4dc_50= Plotter("switch_data_27_02_2018/s4/time_sweep_s4_dc_50.txt")
    s4dc_98= Plotter("switch_data_27_02_2018/s4/time_sweep_s4_dc_98.txt")
    
    plt.title("Switch 4 time sweep comparison")
    plt.xlabel("Duty cycle")
    plt.ylabel("Voltage [V]")
    
    plt.plot(s4dc_1.x(), s4dc_1.y(), label="1")
    plt.plot(s4dc_50.x(), s4dc_50.y(), label="50")
    plt.plot(s4dc_98.x(), s4dc_98.y(), label="98")
    
    plt.legend(loc=1)
    plt.show()
    
    
    
def all_switches_1dc_time_comparison():
    
    plt.rcParams.update({'font.size': 20})
    
    s1dc_1= Plotter("switch_data_27_02_2018/s1/time_sweep_s1_dc_1_01mar.txt")
    s2dc_1= Plotter("switch_data_27_02_2018/s2/time_sweep_s2_dc_1.txt")
    s3dc_1= Plotter("switch_data_27_02_2018/s3/time_sweep_s3_dc_1_26feb.txt")
    s4dc_1= Plotter("switch_data_27_02_2018/s4/time_sweep_s4_dc_1.txt")
    s5dc_1= Plotter("switch_data_27_02_2018/s5/time_sweep_s5_dc_1.txt")
    s6dc_1= Plotter("switch_data_27_02_2018/s6/time_sweep_s6_dc_1.txt")
    s7dc_1= Plotter("switch_data_27_02_2018/s7/time_sweep_s7_dc_1.txt")
    s8dc_1= Plotter("switch_data_27_02_2018/s8/time_sweep_s8_dc_1.txt")

    
    plt.title("Switch comparison 1% duty cycle")
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    
    plt.plot(s1dc_1.x(), s1dc_1.y(), label="s1")
    plt.plot(s2dc_1.x(), s2dc_1.y(), label="s2")
    plt.plot(s3dc_1.x(), s3dc_1.y(), label="s3")
    plt.plot(s4dc_1.x(), s4dc_1.y(), label="s4")
    plt.plot(s5dc_1.x(), s5dc_1.y(), label="s5")
    plt.plot(s6dc_1.x(), s6dc_1.y(), label="s6")
    plt.plot(s7dc_1.x(), s7dc_1.y(), label="s7")
    plt.plot(s8dc_1.x(), s8dc_1.y(), label="s8")
    
    plt.legend(loc=1)
    plt.show()


def all_switches_50_98dc_time_comparison():
    
    plt.rcParams.update({'font.size': 20})
    
    s1dc_1= Plotter("switch_data_27_02_2018/s1/time_sweep_s1_dc_50_01mar.txt")
    s2dc_1= Plotter("switch_data_27_02_2018/s2/time_sweep_s2_dc_50.txt")
    s3dc_1= Plotter("switch_data_27_02_2018/s3/time_sweep_s3_dc_50_26feb.txt")
    s4dc_1= Plotter("switch_data_27_02_2018/s4/time_sweep_s4_dc_50.txt")
    s5dc_1= Plotter("switch_data_27_02_2018/s5/time_sweep_s5_dc_50.txt")
    s6dc_1= Plotter("switch_data_27_02_2018/s6/time_sweep_s6_dc_50.txt")
    s7dc_1= Plotter("switch_data_27_02_2018/s7/time_sweep_s7_dc_50_01mar.txt")
    s8dc_1= Plotter("switch_data_27_02_2018/s8/time_sweep_s8_dc_50.txt")

    plt.plot(s1dc_1.x(), s1dc_1.y(), label="s1", color="b")
    plt.plot(s2dc_1.x(), s2dc_1.y(), label="s2", color="g")
    plt.plot(s3dc_1.x(), s3dc_1.y(), label="s3", color="r")
    plt.plot(s4dc_1.x(), s4dc_1.y(), label="s4", color="c")
    plt.plot(s5dc_1.x(), s5dc_1.y(), label="s5", color="m")
    plt.plot(s6dc_1.x(), s6dc_1.y(), label="s6", color="y")
    plt.plot(s7dc_1.x(), s7dc_1.y(), label="s7", color="k")
    plt.plot(s8dc_1.x(), s8dc_1.y(), label="s8", color="0.75")
    
    s1dc_1= Plotter("switch_data_27_02_2018/s1/time_sweep_s1_dc_98_01mar.txt")
    s2dc_1= Plotter("switch_data_27_02_2018/s2/time_sweep_s2_dc_98.txt")
    s3dc_1= Plotter("switch_data_27_02_2018/s3/time_sweep_s3_dc_98_26feb.txt")
    s4dc_1= Plotter("switch_data_27_02_2018/s4/time_sweep_s4_dc_98.txt")
    s5dc_1= Plotter("switch_data_27_02_2018/s5/time_sweep_s5_dc_98.txt")
    s6dc_1= Plotter("switch_data_27_02_2018/s6/time_sweep_s6_dc_98.txt")
    s7dc_1= Plotter("switch_data_27_02_2018/s7/time_sweep_s7_dc_98_01mar.txt")
    s8dc_1= Plotter("switch_data_27_02_2018/s8/time_sweep_s8_dc_98_01mar.txt")

    
    plt.title("Switch time sweep comparison 50%, 98% duty cycle")
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    
    plt.plot(s1dc_1.x(), s1dc_1.y(), color="b")
    plt.plot(s2dc_1.x(), s2dc_1.y(), color="g")
    plt.plot(s3dc_1.x(), s3dc_1.y(), color="r")
    plt.plot(s4dc_1.x(), s4dc_1.y(), color="c")
    plt.plot(s5dc_1.x(), s5dc_1.y(), color="m")
    plt.plot(s6dc_1.x(), s6dc_1.y(), color="y")
    plt.plot(s7dc_1.x(), s7dc_1.y(), color="k")
    plt.plot(s8dc_1.x(), s8dc_1.y(), color="0.75")
    
    plt.legend(loc=1)
    plt.show()

#pwm_comparison_no_dz()
#s4_time_comparison()
# time_comparison_dc_50()

def pwm_raw():
    raw= Plotter("pwm_output_09_02/N=100-no_optoswitch09_feb.txt")
    plt.rcParams.update({'font.size': 20})
    
    plt.title("Pi PWM board raw output")
    plt.xlabel("Duty cycle [%]")
    plt.ylabel("Voltage [V]")
    
    plt.plot(raw.x(), 3.3*raw.y()/2**15, "bo-")
    
    plt.legend(loc=1)
    plt.show()
    
    
def pwm_low():
    raw= Plotter("optoswitch_output_16_02/100_16_02_0.txt")
    plt.rcParams.update({'font.size': 20})
    
    plt.title("Average smoother circuit output, input 3.9V")
    plt.xlabel("Duty cycle [%]")
    plt.ylabel("Voltage [V]")
    
    plt.plot(raw.x(), raw.y(), "go-")
    
    plt.legend(loc=1)
    plt.show()    