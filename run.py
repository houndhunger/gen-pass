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

def start():
    exsettings = {
    "L": 15,  # Password Length
    "U": 'Yes',  # Use uppercase
    "O": 'Yes',  # Use lowercase
    "N": 'No',  # Use numbers
    "S": 'No',  # Use special characters
    "G": ''  # Generated Password
    }

    settings = {
    "L": {"min": 8, "max": 20},  # Password Length
    "U": {"value": "Yes", "min": 5, "max": 10},  # Use uppercase
    "O": {"value": "Yes", "min": 5, "max": 10},  # Use lowercase
    "N": {"value": "No", "min": 5, "max": 10},   # Use numbers
    "S": {"value": "No", "min": 5, "max": 10},   # Use special characters
    "G": {"value": ""}                  # Generated Password
    }

    #print(settings2["U"]["value"])


    loop(settings)
    end()

def loop(settings):
    """
    Keeps program looping till the End of Program
    Adds extra blank rows to fill the screen to achieve page effect
    Displays Status message and Input
    """
    valid = False
    inp = ""
    message = ""

    while True:
        printed_rows = 14 #increase by every extra print - row

        rows, columns = get_terminal_size()

        ### building page ###
        front_page(settings)
        if message != "":
            printed_rows += 6 #Edit when different Message row count are introduced
        #blank rows to fill the terminal
        for i in (range(rows - printed_rows)):
            print("")
        
        #print(f'valid: {valid}, message: "{message}"')

        #print("Terminal width:", columns)
        #print(f'Terminal height: {rows}')
        #print(f'Printed rows: {printed_rows}')

        if message != "":
            print(f'\nStatus message:\n{message}\n')

        inp = input('Choose action: ')
        inp = inp.upper()
        valid, message = input_valid(inp)

        inp = inp.upper()
        if inp == 'L':
            pass
        elif inp in ('U', 'O', 'N', 'S'):
            settings[inp]["value"] = flip_yes_no(settings[inp]["value"])
        elif inp == 'G':
            settings[inp]["value"] = generate_password(settings)
        elif inp == 'E':
            break;  

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

def end():
        print('\n***\nEnding Password Generator.\nMemory has been cleared.\nStay safe and Goodbye.')

def front_page(settings):
    """
    Display front page containing: Settings info, Action options
    """
    #use when working with google sheet is required
    #settings = SHEET.worksheet('settings')
    #data = settings.get_all_values()
    #print(data)

    print("*** Password Generator ***")
    print("")
    print("* Settings *")
    """
    print(f'[L] Password Length: Min:<{settings["L"]["min"]}>  Max:<{settings["L"]["max"]}>')
    print(f'[U] Use uppercase:<{settings["U"]["value"]}>  Min:<{settings["U"]["min"]}>  Max:<{settings["U"]["max"]}>')
    print(f'[O] Use lowercase:<{settings["O"]["value"]}>  Min:<{settings["O"]["min"]}>  Max:<{settings["O"]["max"]}>')
    print(f'[N] Use Numbers:<{settings["N"]["value"]}>  Min:<{settings["N"]["min"]}>  Max:<{settings["N"]["max"]}>')
    print(f'[S] Use special characters:<{settings["S"]["value"]}>  Min:<{settings["S"]["min"]}>  Max:<{settings["S"]["max"]}>')
    """
    # Format the settings as a list of lists for tabulate
    settings_table = [
    ["[L] Password Length", "", f"<{settings['L']['min']}>", f"<{settings['L']['max']}>"],
    ["[U] Use uppercase", f"<{settings['U']['value']}>", f"<{settings['U']['min']}>", f"<{settings['U']['max']}>"],
    ["[O] Use lowercase", f"<{settings['O']['value']}>", f"<{settings['O']['min']}>", f"<{settings['O']['max']}>"],
    ["[N] Use Numbers", f"<{settings['N']['value']}>", f"<{settings['N']['min']}>", f"<{settings['N']['max']}>"],
    ["[S] Use special characters", f"<{settings['S']['value']}>", f"<{settings['S']['min']}>", f"<{settings['S']['max']}>"],
    ]
 
    print(tabulate(settings_table, headers=["Parameter:", "Value:", "Min:", "Max:"]))
    print(f'Generated password: {settings["G"]["value"]}')
    print("")
    print("[G] Generate Passowrd, [E] End Program")

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
    
    return table
    

def input_valid(inp):
    """
    Checks if user input is valid, returns true if it is, if not it will return message
    """
    message = ""

    if inp in ('L', 'U', 'O', 'N', 'S', 'G', 'E'):
        return True, message
    else:
        return False, "Input value is invalid. \nType in 'L' 'U', 'O', 'N', 'S', 'G', 'E' \nor 'l' 'u', 'o', 'n', 's', 'g', 'e'."

import os
def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)


"""
Start Password Generator Program
"""
start()
