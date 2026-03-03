# Imports.
from pyvisa import util
from pyvisa.resources.tcpip import TCPIPSocket

# Maximum readable chunk size.
MAX_CHUNK_SIZE = 800000

def read_mpm_data(mpm_instance, command: str, data_point: int, set_read_termination: str = '\n') -> list:
    """Read the logging data from MPM."""
    read_count_additional_factor = isinstance(mpm_instance, TCPIPSocket)

    # Validate the data point.
    if data_point < 1:
        return []

    # Estimate the size of the incoming IEEE 488.2 binary block:
    # - 4 bytes per data point
    # - 2 bytes for the block header start
    # - 1 byte for separator (optional)
    # - digits for the length specifier (log10(count))
    read_count = (len(str(data_point * 4)) + 2 + data_point * 4) + read_count_additional_factor

    # Set the termination character to an empty string.
    mpm_instance.read_termination = None

    # Write the command.
    mpm_instance.write(command)

    # Read the raw data and convert a block in the IEEE format into an iterable of numbers.
    response = util.from_ieee_block(
        mpm_instance.read_bytes(count=read_count, chunk_size=MAX_CHUNK_SIZE)
    )
    data = [n for n in response]

    # Set the termination character back to default.
    mpm_instance.read_termination = set_read_termination

    return data
