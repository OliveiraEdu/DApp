#The amount argument is a uint256 number encoded in hex (also, left-padded)

def decimal_to_padded_hexadecimal(num):
    # Convert integer to hexadecimal and remove the '0x' prefix
    hex_string = hex(num)[2:]

    # Calculate the number of zeroes to pad
    num_zeroes = 64 - len(hex_string)

    # Pad zeroes to the left
    padded_hex_string = '0' * num_zeroes + hex_string

    return padded_hex_string.upper()  # Convert to uppercase for consistency

# Example usage
decimal_number = 1000
padded_hexadecimal = decimal_to_padded_hexadecimal(decimal_number)
print(padded_hexadecimal)
