# Imports.
from pyvisa import util
import numpy as np

# Maximum readable chunk size.
MAX_CHUNK_SIZE = 800000

def read_tsl_data(tsl_instance, command: str, data_point: int, set_read_termination: str = '\r\n') -> list:
    """Read the logging data from TSL."""

    # Validate the data point.
    if data_point < 1:
        return []

    # Estimate the size of the incoming IEEE 488.2 binary block:
    # - 4 bytes per data point
    # - 2 bytes for the block header start
    # - 1 byte for separator (optional)
    # - digits for the length specifier (log10(count))
    read_count = len(str(data_point * 4)) + 2 + data_point * 4

    # Set the termination character to an empty string.
    tsl_instance.read_termination = ''

    # Write the command.
    tsl_instance.write(command)

    # Read the raw data and convert a block in the IEEE format into an iterable of numbers.
    response = util.from_ieee_block(
        tsl_instance.read_bytes(count=read_count, chunk_size=MAX_CHUNK_SIZE),
        datatype='i'
    )

    # Round the response to 4 decimal places.
    data = [round(n / 10000, 4) for n in response]

    # Set the termination character back to default.
    tsl_instance.read_termination = set_read_termination

    return data
