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
    return 'Choose next action: '

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

    total_min = sum(data['min'] for data in settings.values() if 'min' in data)
    if total_min - settings['L']['min'] > settings['L']['max']:
        #Sum of Mininals is bigger then Maximal Password Length. Change Settings to satisfy this condition.
        pass
    else:
        #  settings['L']['max'] * settings['U']['min'] * Radnom : something liek this
        pass


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
    f"<{settings['S']['max'] if settings['S']['value'] != 'No' else '-'}>"],
    ]

    print(tabulate(settings_table, headers=["Action key:", "Action:", "Yes/No:", "Min:", "Max:"]))

    return 10
    
def password_section(password):
    print("")
    print("[G] Generate Passowrd     [E] End Program     [\\] Cancel")
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

def build_screen(settings, password, input_message):
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
        input_value = build_screen(settings, password, input_message)

        # Check input
        try:
            input_value = int(input_value)
            if (input_value >= 1 or input_value <= 1024) and (input_value >= settings[action]['min']):
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
                input_message += f"\nPlease enter Maximum count: "
            elif input_value == '':
                continue
            else:
                input_message = action_section(settings[action])
                input_message += f"\nInvalid value!"
                input_message += f"\nPlease enter Maximum count between 1 and 1024 and bigger then Minimum: "
    return settings, input_message

def screen_and_get_min(settings, password, input_value, input_message, action):
    while True:
        input_value = build_screen(settings, password, input_message)

        # Check input
        try:
            input_value = int(input_value)
            if input_value >= 1 or input_value <= 1024:
                settings[action]['min'] = input_value
                input_message = action_section(settings[action])
                input_message += f"\nYou set Minimum count to {settings[action]['min']}."
                input_message += f"\nPlease enter Maximum count: "
                settings, input_message = screen_and_get_max(settings, password, input_value, input_message, action)
                break
            else:
                input_message = action_section(settings[action])
                input_message += f"\nInvalid value <{input_value}>!"
                input_message += f"\nPlease enter Minimum count between 1 and 1024: "  
        except ValueError:
            if input_value == '\\':
                input_message = action_section(settings[action])
                input_message += f"\nYou cancelled {settings[action]['name']} action."
                input_message += f"\n{default_input_message()}"
                break
            elif input_value == '':
                continue
            else:
                input_message = action_section(settings[action])
                input_message += f"\nInvalid value!"
                input_message += f"\nPlease enter Minimum count between 1 and 1024: "
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
            input_message += f"\nPlease enter Minimum count: "
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
             pass
        else:
            input_message = action_section(settings[action])
            input_message += f"\nInvalid key!"
            input_message += f"\nPlease enter 'Y' for Yes or 'N' for No: "
            #if input_value in ('Y', 'N'):
            #    input_value = action
    return settings, input_message

def screen_and_get_action(settings):
    """
    Keeps program looping till the End of Program
    """
    password = ""
    input_message = default_input_message()
    input_value = ""

    while True:
        input_value = build_screen(settings, password+"act", input_message)

        # Check input
        if input_value == 'L':
            input_message = action_section(settings[input_value])  
            input_message += f"\n"
            input_message += f"\nPlease enter Minimum count: "
            settings, input_message = screen_and_get_min(settings, password, input_value, input_message, input_value)
        elif input_value in ('U', 'O', 'N', 'S'):
            input_message = action_section(settings[input_value])  
            input_message += f"\nDo you want to use {settings[input_value]['name']}?"
            input_message += f"\nPlease enter 'Y' for Yes or 'N' for No:  "
            settings, input_message = screen_and_get_yes_no(settings, password, input_value, input_message, input_value)
        elif input_value == 'G':
            input_message = f"\nPasswrod Has been Generated."
            input_message += f"\n{default_input_message()}"
            password = generate_password(settings)
        elif input_value == '':
             pass
        elif input_value == 'E':
            break
        else:
            input_message = f"Invalid key! Plese Enter the key"
            input_message += f"\neather uppercase 'L', 'U', 'O', 'N', 'S', 'G', 'E'"
            input_message += f"\nor lowercase 'l', 'u', 'o', 'n', 's', 'g', 'e':"

def end():
        print("\n*** \nEnding Password Generator. \nMemory has been cleared. \nStay safe and Goodbye.")

def main():
    settings = {
    'L': {'name': 'Password Length', 'min': 8, 'max': 20},  # Password Length
    'U': {'name': 'Uppercase', 'value': 'Yes', 'min': 5, 'max': 10},  # Use uppercase
    'O': {'name': 'Lowercase', 'value': 'Yes', 'min': 5, 'max': 10},  # Use lowercase
    'N': {'name': 'Numbers', 'value': 'No', 'min': 5, 'max': 10},   # Use numbers
    'S': {'name': 'Special characters', 'value': 'No', 'min': 5, 'max': 10},   # Use special characters
    'G': {'name': 'Generate Passowrd', 'value': ''}                  # Generated Password
    }

    screen_and_get_action(settings)
    end()

"""
Start Password Generator Program
"""
if __name__ == "__main__":
    main()
