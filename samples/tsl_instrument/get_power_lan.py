"""
Script to retrieve TSL power data via LAN communication using PyVISA.
"""

import pyvisa
from read_data import read_tsl_data

# Create a VISA resource manager to manage instrument communication
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

# Query the number of power monitor data points available.
data_point = int(tsl.query(':READout:POINts?'))
print("Available data points: ", data_point)

# Get the power monitor data.
power_data = read_tsl_data(tsl, ':READout:DATa:POWer?', data_point)
print("Power monitor data length: ", len(power_data))
