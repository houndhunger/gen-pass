"""
This script generates passwords or keys ranging from 1 to 100 passwords
in length or 1 to 4096 characters. The script fills the entire terminal 
screen.

Note:
When generating multiple passwords or longer keys, maintaining screen integrity
is not possible on a terminal with dimensions less then 24 rows and 80 columns.
The script optimally displays on terminals with 28 lines and more with one 
password up to 80 characters in length.

The "SUM of Minimum and Maximum" provides a check to ensure that the sum of
minimum values does not exceed the maximum password length, and vice versa.
Adjust min and max settings to satisfy this condition. If the variables 
do not meet this condition, an exclamation mark ('!') is displayed.

Operations and keys are dynamically shown based on the active operation.
"""

import calculations
import validate

def end():
    """
    End of script
    """
    print(f"\n*** \nEnding Password Generator. " +\
    f"\nStay safe and Goodbye.")

def main():
    """
    Main function of the script which sets settings, 
    starts main screen, where whole process goes
    and ends script.
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
    #main screen of the script
    validate.screen_and_get_operation(settings)
    end()

"""
Start Password Generator Script
"""
if __name__ == "__main__":
    main()
