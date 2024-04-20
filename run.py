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
Start Password Generator Program
"""
if __name__ == "__main__":
    main()
