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
    settings = {
    "L": 15,  # Password Length
    "U": 'Yes',  # Use uppercase
    "O": 'Yes',  # Use lowercase
    "N": 'No',  # Use numbers
    "S": 'No',  # Use special characters
    "G": ''  # Generated Password
    }
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
        printed_rows = 13 #increase by every extra print - row

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
            settings[inp] = flip_yes_no(settings[inp])
        elif inp == 'G':
            settings[inp] = generate_password(settings)
        elif inp == 'E':
            break;  

def flip_yes_no(value):
    value = 'No' if value == 'Yes' else 'Yes'
    return value

import random
import string
def generate_password(settings):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(settings['L']))
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
    print("Settings:")
    print(f'[L] Password Length: <{settings["L"]}>')
    print(f'[U] Use uppercase: <{settings["U"]}>')
    print(f'[O] Use lowercase: <{settings["O"]}>')
    print(f'[N] Use Numbers: <{settings["N"]}>')
    print(f'[S] Use special characters: <{settings["S"]}>')
    print("")
    print(f'Generated password: <{settings["G"]}>')
    print("")
    print("[G] Generate Passowrd, [E] End Program")

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
