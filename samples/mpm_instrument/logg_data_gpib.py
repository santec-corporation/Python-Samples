"""
Script to retrieve MPM logging data via GPIB communication using PyVISA.
"""

import pyvisa
from read_data import read_mpm_data

# Create a resource manager instance to handle VISA connections
rm = pyvisa.ResourceManager()

# Define the GPIB resource address of the instrument
gpib_resource = "GPIB1::15::INSTR"

# Open a connection to the instrument using the specified GPIB address
mpm = rm.open_resource(gpib_resource)
mpm.read_termination = '\n'

# Query and print the identification string of the connected instrument
idn = mpm.query('*IDN?')
print("IDN: ", idn)

# Query the number of log entries stored in the instrument
count = int(mpm.query('LOGN?'))
print("Logging count: ", count)

# Get the log data.
log_data = read_mpm_data(mpm, 'LOGG? 0,1', count)
print("Log data length: ", len(log_data))
