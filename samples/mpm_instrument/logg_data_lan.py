"""
Script to retrieve MPM logging data via LAN communication using PyVISA.
"""

import pyvisa
from read_data import read_mpm_data

# Create a VISA resource manager to handle communication with instruments
rm = pyvisa.ResourceManager()

# Define the LAN socket address of the instrument (IP, port)
lan_resource = "TCPIP0::192.168.1.161::5000::SOCKET"

# Open a socket connection to the instrument with the specified read termination character
mpm = rm.open_resource(lan_resource, read_termination='\r')

# Query and print the identification string of the connected instrument
idn = mpm.query('*IDN?')
print("IDN: ", idn)

# Query the number of log entries stored in the instrument
count = int(mpm.query('LOGN?'))
print("Logging count: ", count)

# Get the log data.
log_data = read_mpm_data(mpm, 'LOGG? 0,1', count, '\r')
print("Log data length: ", len(log_data))
