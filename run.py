################################################################################
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread 
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('password_gen')

def default_input_message():
    message = "Choose next action: "
    return message

"""
checks if xsel is installed for clypbosrd op
"""

import os # for get_terminal_size()

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


def sum_min_max(settings):
    char_type = ('U', 'O', 'N', 'S')
    sum_lmin = 0
    sum_lmax = 0
    for char in char_type:
        if settings[char]['value'] == 'Yes':
            sum_lmin += settings[char]['min']
            sum_lmax += settings[char]['max']
    settings['SUM']['min'] = sum_lmin
    settings['SUM']['max'] = sum_lmax
    return settings, sum_lmin, sum_lmax

################################################################################
import random
import string
def generate_password(settings):

    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    punctuation = string.punctuation

    password = ''

    settings, sum_lmin, sum_lmax = sum_min_max(settings)

    if sum_lmin > settings['L']['min']:
        length_min = sum_lmin
    else:
        length_min = settings['L']['min']

    if  sum_lmax > settings['L']['max']:
        length_max = sum_lmax
    else:
        length_min = settings['L']['max']

    """
    Add this to input message

    if sum_lmin <= settings['L']['max'] and sum_lmax >= settings['L']['min'] and length_max - length_min >= 0:
        print(f"length_min: {length_min}")
        print(f"length_max: {length_max}")
    else:
        print("Sum of Mininals is bigger then Maximal Password Length. Change Settings to satisfy this condition.")
    """
################################################################################
    char_type = ('U', 'O', 'N', 'S')
    password_components = {
        'U': letters.upper(), 'O': letters.lower(), 
        'N': digits, 'S': punctuation
        }
    
    passwords = ""

    for i in range(settings['B']['value']):
        password = ""
        # Generate password components
        for char in char_type:
            if settings[char]["value"] == 'Yes':
                password += ''.join(random.choices(password_components[char],
                 k=settings[char]['min']))

        #password = ''.join(password_list)

        password_length = random.randint(length_min, length_max)

        # Calculate the remaining length for the password
        remaining_length = password_length - sum_lmin

        # Get character types with 'Yes' values in settings
        yes_char_types = [
            char for char in char_type 
            if settings[char]["value"] == 'Yes'
            ]

        # Fill the remaining length with random characters
        if remaining_length > 0:
            remaining_characters = ''.join(
                random.choices(
                    ''.join(password_components[char] 
                    for char in yes_char_types), 
                    k=remaining_length
                )
            )
            password += remaining_characters

        # Shuffle the password to ensure randomness
        password_list = list(password)
        random.shuffle(password_list)
        password = ''.join(password_list)
        passwords += password + "\n"

    return passwords

def tabulate(table, headers):
    # Combine the headers with the table data
    all_data = [headers] + table

    # Find the maximum width of each column
    column_widths = [
        max(len(str(row[i])) for row in all_data) for i in range(len(headers))
        ]

    # Format each row with extra spaces to achieve aligned look
    formatted_table = []
    for row in all_data:
        formatted_row = [
            str(cell).ljust(column_widths[i]) for i, cell in enumerate(row)
            ]
        formatted_table.append(formatted_row)

    table = ""
    # Print the formatted table
    for row in formatted_table:
        table +=" | ".join(row) + "\n"
    
    return table[:-1]

def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

def count_newlines(string):
    return string.count("\n") + 1

def print_and_count(string):
    print(string)
    return count_newlines(string)

def header_section():  
    #for terminal row smaller then 26 to mainitain screen integrity
    #rows, columns = get_terminal_size()
    #if rows <= 26:
    #    return 0
    #else:
    print("*** Password Generator ***")
    return 1

################################################################################
def settings_section(settings):
    """
    Display front page containing: Settings info, Action options
    """
    rows_count = 0

    #for terminal row smaller then 26 to mainitain screen integrity
    #rows, columns = get_terminal_size()
    #if rows > 26:
    print("")
    rows_count += 1

    print("* Settings *")

    # Format the settings as a list of lists for tabulate
    settings_table = [
    ["[L]", settings['L']['name'], "-", 
    f"<{settings['L']['min']}>", f"<{settings['L']['max']}>"],
       
    ["[B]", settings['B']['name'], f"<{settings['B']['value']}>",
    "-", "-"],

    ["[U]", settings['U']['name'], f"<{settings['U']['value']}>", 
    f"<{settings['U']['min'] if settings['U']['value'] != 'No' else '-'}>", 
    f"<{settings['U']['max'] if settings['U']['value'] != 'No' else '-'}>"],  

    ["[O]", settings['O']['name'], f"<{settings['O']['value']}>", 
    f"<{settings['O']['min'] if settings['O']['value'] != 'No' else '-'}>", 
    f"<{settings['O']['max'] if settings['O']['value'] != 'No' else '-'}>"],
    
    ["[N]", settings['N']['name'], f"<{settings['N']['value']}>", 
    f"<{settings['N']['min'] if settings['N']['value'] != 'No' else '-'}>", 
    f"<{settings['N']['max'] if settings['N']['value'] != 'No' else '-'}>"],
    
    ["[S]", settings['S']['name'], f"<{settings['S']['value']}>", 
    f"<{settings['S']['min'] if settings['S']['value'] != 'No' else '-'}>", 
    f"<{settings['S']['max'] if settings['S']['value'] != 'No' else '-'}>"]
    ]

    #for terminal row smaller then 24 to mainitain screen integrity
    #rows, columns = get_terminal_size()
    #if rows > 24:
    settings_table.insert(0, ["---"] * 5)
    settings_table.insert(3, ["---"] * 5)

    print(tabulate(settings_table, headers = [
        "Action key:", "Action:", "Yes/No:", "Min: ", "Max: "
        ]))
    rows_count += count_newlines(tabulate(settings_table, headers = [
        "Action key:", "Action:", "Yes/No:", "Min: ", "Max: "
        ])) + 1 # +1 for headers
    return rows_count

def sum_section(settings):
    print("")
    print(f"SUM of Minimum and Maximum (<Yes> only):   ",
    f" Min. {settings['SUM']['min'] if settings['SUM']['min'] <= settings['L']['max'] else "!" + str(settings['SUM']['min'])}",
    f" Max. {settings['SUM']['max'] if settings['SUM']['max'] >= settings['L']['min'] else "!" + str(settings['SUM']['max'])}")
    return 2

def actions_section():
    print("")
    print("[G] Generate Password   " + (
        "[C] Copy to clipboard   [R] Clear clipboard" 
        if is_xsel_installed() or is_pyperclip_installed() 
        else ""
        ))
    print("[E] End Program   [Enter] Skip   [\\] Cancel")
    print("")
    print("Legend:   [] Key   <> Variable")
    return 5

def password_section(password):
    print("")
    print("* Generated password *")
    print(password) 
    return count_newlines(password) + 2

def blank_lines_section(rows_count):
    #get terminal size
    rows, columns = get_terminal_size() 
    #columns - I might not need them, except for "print string width" check...
    #blank lines to fill the the screen
    for i in (range(rows - rows_count)):
        print("")

def build_screen(settings, password, input_message):
    """
    building screen from top - header to the bottom  
        - input, filling the whole screen
    """
    rows_count = 0 #increase by every extra print - row
    rows_count += header_section() # 1 line
    rows_count += actions_section() # 5 lines
    if count_newlines(input_message) == 1:
        rows_count += settings_section(settings) # 10 lines
    else:
        pass # action_section(settings)
    rows_count += sum_section(settings) # 2 lines
    rows_count += password_section(password) # 2+ lines
    rows_count += count_newlines(input_message) # 1 / 4 lines


    #blank lines to fill the the screen
    blank_lines_section(rows_count) 
    


    #input message
    input_value = input(input_message).upper()
    return input_value

def action_status(action):
    status = f"Action status:"
    # Check if 'value' key exists in the action dictionary
    if 'value' in action:
        status += f" {action['name']} <{action['value']}>,"  
        # Check if 'value' is 'No' and return status if it is
        if action['value'] == 'No':
            return status
    # Add 'Min' and 'Max' to the status
    status += f" Min: <{action.get('min', '')}>, Max: <{action.get('max', '')}>."
    return status

def action_section(action):
    #Action Name - Header
    section = f"* {action['name']} *\n"
    #Action status
    section += f"{action_status(action)}\n"
    return section    

def input_valid(input_value):
    """
    Checks if user input is valid, returns true if it is, if not it will return message
    """
    message = ""

    if input_value in ('L', 'U', 'O', 'N', 'S', 'G', 'E'):
        return True, message
    else:
        return False, "Input value is invalid. \nType in 'L' 'U', 'O', 'N', 'S', 'G', 'E' \nor 'l' 'u', 'o', 'n', 's', 'g', 'e'."

def screen_and_get_max(settings, password, input_value, input_message, action):
    while True:
        settings, sum_lmin, sum_lmax = sum_min_max(settings)
        input_value = build_screen(settings, password, input_message)

        # Check input
        try:
            input_value = int(input_value)
            if (input_value >= 1 and input_value <= 1024) and (input_value >= settings[action]['min']):
                settings[action]['max'] = input_value
                input_message = action_section(settings[action])
                input_message += f"\nYou set Maximum value to {settings[action]['max']}."
                input_message += f"\n{default_input_message()}"
                break
        except ValueError:
            if input_value == '\\' and int(settings[action]['min']) <= int(settings[action]['max']):
                input_message = action_section(settings[action])
                input_message += f"\nYou cancelled {settings[action]['name']} action."
                input_message += f"\n{default_input_message()}"
                break
            elif int(settings[action]['min']) > int(settings[action]['max']):
                input_message = action_section(settings[action])
                input_message += f"\nMinimum cannot be more then Maximum."
                input_message += f"\nPlease enter Maximum count: <{settings[action]['max']}> "
            elif input_value == '':
                input_message = action_section(settings[action])
                input_message += f"\nYou confirmed previus Maximum value {settings[action]['max']}."
                input_message += f"\n{default_input_message()}"
                break
            else:
                input_message = action_section(settings[action])
                input_message += f"\nInvalid value!"
                input_message += f"\nPlease enter Maximum count between 1 and 1024 and bigger then Minimum: "
    return settings, input_message

def screen_and_get_min(settings, password, input_value, input_message, action):
    while True:
        settings, sum_lmin, sum_lmax = sum_min_max(settings)
        input_value = build_screen(settings, password, input_message)

        # Check input
        try:
            input_value = int(input_value)
            if input_value >= 1 and input_value <= 1024:
                settings[action]['min'] = input_value
                input_message = action_section(settings[action])
                input_message += f"\nYou set Minimum count to {settings[action]['min']}."
                input_message += f"\nPlease enter Maximum count: <{settings[action]['max']}> "
                settings, input_message = screen_and_get_max(settings, password, input_value, input_message, action)
                break
            else:
                input_message = action_section(settings[action])
                input_message += f"\nInvalid value <{input_value}>!"
                input_message += f"\nPlease enter Minimum count (1-1024): <{settings[action]['min']}> "  
        except ValueError:
            if input_value == '\\':
                input_message = action_section(settings[action])
                input_message += f"\nYou cancelled {settings[action]['name']} action."
                input_message += f"\n{default_input_message()}"
                break
            elif input_value == '':
                input_message = action_section(settings[action])
                input_message += f"\nYou confirmed previous Minimum count {settings[action]['min']}."
                input_message += f"\nPlease enter Maximum count: <{settings[action]['max']}> "
                settings, input_message = screen_and_get_max(settings, password, input_value, input_message, action)
                break
            else:
                input_message = action_section(settings[action])
                input_message += f"\nInvalid value!"
                input_message += f"\nPlease enter Minimum count (1-1024): <{settings[action]['min']}> "
    return settings, input_message

def screen_and_get_yes_no(settings, password, input_value, input_message, action):
    while True:
        #build screen
        input_value = build_screen(settings, password, input_message)

        #check inupt
        if input_value == 'Y':
            settings[action]['value'] = 'Yes'
            input_message = action_section(settings[action])
            input_message += f"\nYou selected 'Yes'."
            input_message += f"\nPlease enter Minimum count: <{settings[action]['min']}> "
            settings, input_message = screen_and_get_min(settings, password, input_value, input_message, action)
            break
        elif input_value == 'N':
            settings[action]['value'] = 'No'
            #input_message = action_section(settings[action])
            input_message += f"\nYou selected 'No'."
            input_message += f"\n{default_input_message()}"
            break
        elif input_value == '\\':
            input_message = action_section(settings[action])
            input_message += f"\nYou cancelled {settings[action]['name']} action."
            input_message += f"\n{default_input_message()}"
            break
        elif input_value == '':
            if settings[action]['value'] == 'Yes':
                input_message = action_section(settings[action])
                input_message += f"\nYou confirmed previus value 'Yes'."
                input_message += f"\nPlease enter Minimum count: <{settings[action]['min']}> "
                settings, input_message = screen_and_get_min(settings, password, input_value, input_message, action)
                break 
            elif settings[action]['value'] == 'No':
                #input_message = action_section(settings[action])
                input_message += f"\nYou confirmed previus value 'No'."
                input_message += f"\n{default_input_message()}"
                break
        else:
            input_message = action_section(settings[action])
            input_message += f"\nInvalid key!"
            input_message += f"\nPlease enter 'Y' for Yes or 'N' for No: <{settings[action]['value']}> "
            #if input_value in ('Y', 'N'):
            #    input_value = action
    return settings, input_message

def screen_and_get_value(settings, password, input_value, input_message, action):
    while True:
        #build screen
        input_value = build_screen(settings, password, input_message)
        
        # Check input
        try:
            input_value = int(input_value)
            if (input_value >= 1 or input_value <= 100):
                settings[action]['value'] = input_value
                input_message = action_section(settings[action])
                input_message += f"\nYou set generated password count to {settings[action]['value']}."
                input_message += f"\n{default_input_message()}"
                break
        except ValueError:
            if input_value == '\\':
                input_message = action_section(settings[action])
                input_message += f"\nYou cancelled {settings[action]['name']} action."
                input_message += f"\n{default_input_message()}"
                break
            elif input_value == '':
                input_message = action_section(settings[action])
                input_message += f"\nYou confirmed generated password count {settings[action]['value']}."
                input_message += f"\n{default_input_message()}"
                break
            else:
                input_message = action_section(settings[action])
                input_message += f"\nInvalid value!"
                input_message += f"\nPlease enter generated password count between 1 and 100: <{settings[action]['value']}> "
    return settings, input_message

#import pyperclip
#from clipboard import copy_to_clipboard, clear_clipboard
def screen_and_get_action(settings):
    """
    Keeps program looping till the End of Program
    """
    password = ""
    input_message = default_input_message()
    input_value = ""

    while True:
        settings, sum_lmin, sum_lmax = sum_min_max(settings)
        input_value = build_screen(settings, password, input_message)

        # Check input
        if input_value == 'L':
            input_message = action_section(settings[input_value])  
            input_message += f"\n"
            input_message += f"\nPlease enter Minimum count: <{settings[input_value]['min']}> "
            settings, input_message = screen_and_get_min(settings, password, input_value, input_message, input_value)
        elif input_value in ('U', 'O', 'N', 'S'):
            input_message = action_section(settings[input_value])  
            input_message += f"\nDo you want to use {settings[input_value]['name']}?"
            input_message += f"\nPlease enter 'Y' for Yes or 'N' for No: <{settings[input_value]['value']}> "
            settings, input_message = screen_and_get_yes_no(settings, password, input_value, input_message, input_value)
        elif input_value == 'G':
            input_message = f"\nPassword has been generated."
            input_message += f"\n{default_input_message()}"
            password = generate_password(settings)
        elif input_value == 'B':
            input_message = action_section(settings[input_value])  
            input_message += f"\n"
            input_message += f"\nHow many passwords you want to generate (1-100)? <{settings[input_value]['value']}> "
            settings, input_message = screen_and_get_value(settings, password, input_value, input_message, input_value)
        elif input_value == '':
             pass
        elif input_value == 'E':
            break
        else:
            input_message = f"Invalid key! Plese Enter the key"
            input_message += f"\neather uppercase 'L', 'U', 'O', 'N', 'S', 'G', 'E'"
            input_message += f"\nor lowercase 'l', 'u', 'o', 'n', 's', 'g', 'e':"

        """
        elif input_value == 'C':
            input_message = f"\nPassword has been copied to the clipboard."
            input_message += f"\n{default_input_message()}"
            pyperclip.copy(password)
            #copy_to_clipboard(password)
        elif input_value == 'R':
            input_message = f"\nPassword has been cleared from the clipboard."
            input_message += f"\n{default_input_message()}"
            clear_clipboard()
        """

def end():
        print("\n*** \nEnding Password Generator. \nMemory has been cleared. \nStay safe and Goodbye.")

def main():
    settings = {
    'L': {'name': 'Password Length', 'min': 4, 'max': 8},  # Password Length
    'U': {'name': 'Uppercase', 'value': 'No', 'min': 5, 'max': 10},  # Use uppercase
    'O': {'name': 'Lowercase', 'value': 'Yes', 'min': 4, 'max': 5},  # Use lowercase
    'N': {'name': 'Numbers', 'value': 'Yes', 'min': 1, 'max': 2},   # Use numbers
    'S': {'name': 'Special characters', 'value': 'No', 'min': 5, 'max': 10},   # Use special characters
    'B': {'name': 'Batch count', 'value': 1},   # Generated password count
    'SUM': {'name': 'SUM', 'min': 0, 'max': 0}, # Sum
    'SHOW':{'settings': True, 'action': False} # Show or not parts of page
    }

    screen_and_get_action(settings)
    end()

"""
Start Password Generator Program
"""
if __name__ == "__main__":
    main()


"""
sudo apt-get install xsel

sudo apt remove xsel
sudo yum remove xsel
pip uninstall xsel

"""
