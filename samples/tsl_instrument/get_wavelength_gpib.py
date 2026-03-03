"""
Script to retrieve TSL wavelength data via GPIB communication using PyVISA.
"""

import pyvisa
from read_data import read_tsl_data

# Create a VISA resource manager
rm = pyvisa.ResourceManager()

# Define the GPIB resource address of the TSL instrument
gpib_resource = "GPIB0::1::INSTR"

# Open the connection to the TSL device over GPIB
tsl = rm.open_resource(gpib_resource)

# Query the instrument's identification string
idn = tsl.query('*IDN?')
print("IDN: ", idn)

# Query the number of wavelength data points available.
data_point = int(tsl.query(':READout:POINts?'))
print("Available data points: ", data_point)

# Get the wavelength data.
wavelength_data = read_tsl_data(tsl, ':READout:DATa?', data_point)
print("Wavelength data length: ", len(wavelength_data))
