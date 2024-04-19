
# Write your code to expect a terminal of 80 characters wide and 24 rows high



"""
checks if xsel is installed for clypbosrd op
"""

import subprocess
import platform
def is_xsel_installed():
    if platform.system() != 'Linux':
        return False  # xsel is only available on Linux
    try:
        subprocess.run(["xsel", "--version"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_pyperclip_installed():
    try:
        import pyperclip
        return True
    except ImportError:
        return False
  
##### operation_status() not needed - not used
def operation_status(operation):
    status = f"Operation status:"
    # Check if 'value' key exists in the operation dictionary
    if 'value' in operation:
        status += f" {operation['name']} <{operation['value']}>,"  
        # Check if 'value' is 'No' and return status if it is
        if operation['value'] == 'No':
            return status
    # Add 'Min' and 'Max' to the status
    status += f" Min: <{operation.get('min', '')}>, Max: <{operation.get('max', '')}>."
    return status
    
##### operation_section() not needed - not used
def operation_section(operation):
    #Operation Name - Header
    section = f"* {operation['name']} *\n"
    #Operation status
    section += f"{operation_status(operation)}\n"
    return section    

##### input_valid() not needed - not used
def input_valid(inp_value):
    """
    Checks if user input is valid.
    Returns true if it is, if not it will return message
    """
    if inp_value in ('L', 'U', 'O', 'N', 'S', 'G', 'E'):
        return True, ""
    else: ##### is this used? because input varries
        message = ("Input value is invalid. \n"
        "Type in 'L' 'U', 'O', 'N', 'S', 'G', 'E' \n"
        "or 'l' 'u', 'o', 'n', 's', 'g', 'e'.")
        return False, message

import calculations
#import sections
import validate
def end():
        print(f"\n*** \nEnding Password Generator. " +\
        f"\nMemory has been cleared. \nStay safe and Goodbye.")

def main():
    """
    Main function of the program which sets settings, 
    starts main screen, where whole process goes
    and ends program.
    """
    settings = {
    # Password Length
    'L': {'name': 'Password Length', 'min': 4, 'max': 8},  
    # Uppercase
    'U': {'name': 'Uppercase', 'value': 'No', 'min': 5, 'max': 10},
    # Lowercase
    'O': {'name': 'Lowercase', 'value': 'Yes', 'min': 4, 'max': 5},
    # Use numbers  
    'N': {'name': 'Numbers', 'value': 'Yes', 'min': 1, 'max': 2},
    # Use special characters
    'S': {'name': 'Special characters', 'value': 'No', 'min': 5, 'max': 10},
    # Generated password count  
    'B': {'name': 'Batch count', 'value': 1},
    # Check sum for the min and max 
    'SUM': {'name': 'SUM', 'min': 0, 'max': 0},
    # Holds active operation to display crelevant content i.e. key operations
    'ACTIVE-OP': 'HOME'
    }
    #main screen of the program
    validate.screen_and_get_operation(settings)
    end()

"""
Start Password Generator Program
"""
if __name__ == "__main__":
    main()
