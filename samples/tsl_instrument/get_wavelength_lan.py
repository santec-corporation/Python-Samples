"""
Script to retrieve TSL wavelength data via LAN communication using PyVISA.
"""

import pyvisa
from read_data import read_tsl_data

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()

# Define LAN socket resource for TSL (update IP and port if needed)
lan_resource = "TCPIP0::192.168.1.100::5000::SOCKET"

# Open the connection to TSL over LAN
tsl = rm.open_resource(lan_resource, read_termination='\r')

# Set the timeout (in milliseconds)
tsl.timeout = 4000

# Query the instrument's identification string
idn = tsl.query('*IDN?')
print("IDN: ", idn)

# Query the number of wavelength data points available.
data_point = int(tsl.query(':READout:POINts?'))
print("Available data points: ", data_point)

# Get the wavelength data.
wavelength_data = read_tsl_data(tsl, ':READout:DATa?', data_point, '\r')
print("Wavelength data length: ", len(wavelength_data))