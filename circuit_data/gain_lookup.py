# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : gain_lookup.py
# *
# * Author            : Alice Cao
# *
# * Date created      : 4 Feb 2018
# *
# * Purpose           : Lookup table for gain scaling the 16-bit output value of the ADC board.
# *                     
# * Compatible with   : Adafruit ADS1115 16-Bit ADC - 4 Channel with Programmable Gain Amplifier
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

gains = {"2/3":6.144,\
	"1":4.096,\
	"2":2.048,
	"4":1.024,
	"8":0.512,
	"16":0.256}