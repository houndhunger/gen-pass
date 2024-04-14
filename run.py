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
    return 'Choose action: '

    """
    On choosing action U f.e.: 
    Ask for value: Y / N , error & ask again, escape. 
    If Yes, ask for Min, error & ask again, escape. 
    And ask for Max, error & ask again, escape.
    """

def flip_yes_no(value):
    value = 'No' if value == 'Yes' else 'Yes'
    return value

import random
import string
def generate_password(settings):
    #characters = string.ascii_letters + string.digits + string.punctuation
    #password = ''.join(random.choice(characters) for _ in range(settings['L']))
    #return password

    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    punctuation = string.punctuation

    password = ''

    # Generate password components
    if settings['U']["value"] == 'Yes': 
        password += ''.join(random.choices(letters.upper(), k=10))
    if settings['O']["value"] == 'Yes': 
        password += ''.join(random.choices(letters.lower(), k=10))
    if settings['N']["value"] == 'Yes': 
        password += ''.join(random.choices(digits, k=5))
    if settings['S']["value"] == 'Yes': 
        password += ''.join(random.choices(punctuation, k=2))

    # Shuffle the password to ensure randomness
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

def tabulate(table, headers):
    # Combine the headers with the table data
    all_data = [headers] + table

    # Find the maximum width of each column
    column_widths = [max(len(str(row[i])) for row in all_data) for i in range(len(headers))]

    # Format each row with extra spaces to achieve aligned look
    formatted_table = []
    for row in all_data:
        formatted_row = [str(cell).ljust(column_widths[i]) for i, cell in enumerate(row)]
        formatted_table.append(formatted_row)

    table = ""
    # Print the formatted table
    for row in formatted_table:
        table +=" | ".join(row) + "\n"
    
    return table[:-1]

def header_section():
    print("*** Password Generator ***")
    return 1

def settings_section(settings):
    """
    Display front page containing: Settings info, Action options
    """
    #use when working with google sheet is required
    #settings = SHEET.worksheet('settings')
    #data = settings.get_all_values()
    #print(data)

    print("")
    print("* Settings *")

    # Format the settings as a list of lists for tabulate
    settings_table = [
    ["[L]", settings['L']['name'], "", f"<{settings['L']['min']}>", f"<{settings['L']['max']}>"],
    ["[U]", settings['U']['name'], f"<{settings['U']['value']}>", f"<{settings['U']['min']}>", f"<{settings['U']['max']}>"],
    ["[O]", settings['O']['name'], f"<{settings['O']['value']}>", f"<{settings['O']['min']}>", f"<{settings['O']['max']}>"],
    ["[N]", settings['N']['name'], f"<{settings['N']['value']}>", f"<{settings['N']['min']}>", f"<{settings['N']['max']}>"],
    ["[S]", settings['S']['name'], f"<{settings['S']['value']}>", f"<{settings['S']['min']}>", f"<{settings['S']['max']}>"],
    ]
    print(tabulate(settings_table, headers=["Action key:", "Parameter:", "Value:", "Min:", "Max:"]))

    return 10
    
def password_section(password):
    print("")
    print("[G] Generate Passowrd, [E] End Program")
    print("")
    print(f'* Generated password *\n {password}') #later loop thorugh array of passwords

    return 4

def count_newlines(string):
    return string.count("\n")

def print_and_count(string):
    print(string)
    return count_newlines(string)

import os
def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

def blank_lines_section(printed_rows):
    #get terminal size
    rows, columns = get_terminal_size() #columns - I might not need them, except for string width check...
    #blank lines to fill the the screen
    for i in (range(rows - printed_rows)):
        print("")

def build_screen(settings, password, input_message, input_value):
    """
    building screen from top - header to the bottom  - input, filling the whole screen
    """
    printed_rows = 0 #increase by every extra print - row
    printed_rows += header_section() # 1 row
    printed_rows += settings_section(settings) # 10 lines
    printed_rows += password_section(password) # 4 lines

    printed_rows += count_newlines(input_message) # just count input_message lines

    #blank lines to fill the the screen
    blank_lines_section(printed_rows) 

    #input message
    input_value = input(input_message).upper()
    return input_value


def input_valid(input_value):
    """
    Checks if user input is valid, returns true if it is, if not it will return message
    """
    message = ""

    if input_value in ('L', 'U', 'O', 'N', 'S', 'G', 'E'):
        return True, message
    else:
        return False, "Input value is invalid. \nType in 'L' 'U', 'O', 'N', 'S', 'G', 'E' \nor 'l' 'u', 'o', 'n', 's', 'g', 'e'."

def screen_and_get_action(settings):
    """
    Keeps program looping till the End of Program
    """
    password = ""
    input_message = default_input_message()
    input_value = ""

    while True:
        input_value = build_screen(settings, password, input_message, input_value)
                
        # Check input
        if input_value == 'L':
            input_message = "Please enter Minimum count or '\\' for Escape to cancel the action: "
            settings_parameter = screen_and_get_min(settings['L'], input_value, input_message)
        elif input_value in ('U', 'O', 'N', 'S'):
            input_message = "Please enter 'Y', 'N' or '\\' for Escape to cancel the action: "
        elif input_value == 'Y':
            input_message = "Please enter Minimum count or '\\' for Escape to cancel the action: "
        elif input_value == 'N':
            input_message = "Please enter Minimum count or '\\' for Escape to cancel the action: "
        elif isinstance(input_value, int):
            input_message = "Please enter Maximum count or '\\' for Escape to cancel the action: "
        elif input_value == '\\':
            input_message = "You cancelled the action.\n"
            printed_rows += 1
            input_message += default_input_message()
        elif input_value == 'G':
            settings[input_value]["value"] = generate_password(settings)
        elif input_value == '':
             input_message += default_input_message()
        elif input_value == 'E':
            break
        else:
            pass #invalid_inupt() #define this

        """
        if input_value == 'L':
            pass
        elif input_value in ('U', 'O', 'N', 'S'):
            settings[input_value]["value"] = flip_yes_no(settings[input_value]["value"])
        elif input_value == 'G':
            settings[input_value]["value"] = generate_password(settings)
        elif input_value == 'E':
            break;
        """

def screen_and_get_min(parameter, input_value, input_message):
    pass

"""
program_loop
    while loop
        draw page
        check inputs 
            'U', 'O', 'N', 'S': go to program_loop - send Parameter, once nest out, settings gets overwritten
            'Y', 'N', ## - Parameter must be populated
            'G': go beck and do while loop
            'E': or exit

on checking inputs
    define next message
    
screen - header, settings, password, input message

screen_and_get_action
screen_and_get_yes_no
screen_and_get_min
screen_and_get_max
screen_and_get_password

any get_* contains checking input and nest in or out.

"""

def end():
        print('\n***\nEnding Password Generator.\nMemory has been cleared.\nStay safe and Goodbye.')

def main():
    settings = {
    'L': {'name': 'Password Length', 'min': 8, 'max': 20},  # Password Length
    'U': {'name': 'Use uppercase', 'value': 'Yes', 'min': 5, 'max': 10},  # Use uppercase
    'O': {'name': 'Use lowercase', 'value': 'Yes', 'min': 5, 'max': 10},  # Use lowercase
    'N': {'name': 'Use Numbers', 'value': 'No', 'min': 5, 'max': 10},   # Use numbers
    'S': {'name': 'Use special characters', 'value': 'No', 'min': 5, 'max': 10},   # Use special characters
    'G': {'name': 'Generate Passowrd', 'value': ''}                  # Generated Password
    }

    screen_and_get_action(settings)
    end()

"""
Start Password Generator Program
"""
if __name__ == "__main__":
    main()
