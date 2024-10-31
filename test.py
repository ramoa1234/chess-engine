# Given uint64 value
uint64_value = 134217728

def string_to_binary(input_string):
    """Convert each character in the input string to its binary representation."""
    binary_list = []
    
    for char in input_string:
        if char.isdigit():  # Check if the character is a digit
            # Convert the character to an integer and then to binary
            binary_value = format(int(char), '08b')  # Use 8 bits for single digits
            binary_list.append(binary_value)
    
    return binary_list  # Return the list of binary values

# Example usage
input_string = str(uint64_value)  # Convert the uint64 value to string
binary_representation = string_to_binary(input_string)

# Print each binary representation in a new row
for binary in binary_representation:
    print(binary)
