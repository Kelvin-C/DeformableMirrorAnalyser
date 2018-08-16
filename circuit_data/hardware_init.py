# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : hardware_init.py
# *
# * Author            : Alice Cao
# *
# * Date created      : 4 Feb 2018
# *
# * Purpose           : Initialisation of hardware PWM and ADC boards.                     
# *                     
# * Compatible with   : Adafruit 16-Channel 12-bit PCA9685 PWM/Servo Driver
# *                     Adafruit ADS1115 16-Bit ADC - 4 Channel with Programmable Gain Amplifier
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

import Adafruit_PCA9685 # Adafruit PWM board 12-bit
import Adafruit_ADS1x15 # ADC board 16-bit
import ServoPi # ABElectronics PWM board 12-bit

class Adafruit_PWM:
    def __init__(self, fr=1000):
        """ Turn on the PWM with given frequency (fr) """
        self.__ada_pwm = Adafruit_PCA9685.PCA9685() # Initialise the PCA9685 using the default address (0x40)
        self.__ada_pwm.set_pwm_freq(fr)
        self.__fr = fr
    
    def freq(self):
        return self.__fr

    def adapwm(self):
        return self.__ada_pwm
    
class AB_PWM:
    def __init__(self, freq=0):
        """ Turn on the PWM with given frequency (freq) """
        self.__ab_pwm = ServoPi.PWM(0x40)
        self.__ab_pwm.set_pwm_freq(freq)

    def abpwm(self):
        return self.__ab_pwm

class Adafruit_ADC:
    def __init__(self, gain=0):
        """ Turn on the ADC with given gain [2//3, 1, 2, 4, 8, 16] """
        self.__ada_adc = Adafruit_ADS1x15.ADS1115()
        self.__GAIN = gain

        if gain not in [2//3, 1, 2, 4, 8, 16]:
            raise Exception("Invalid gain.")

    def gain(self):
        return self.__GAIN
    
    def adaadc(self):
        return self.__ada_adc