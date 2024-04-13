# Your code goes here.
# You can delete these comments, but do not change the name of this file
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

def program():
    """
    Keeps program running till the End of Program
    """
    end = False
    valid = False
    inp = ""
    message = ""

    while not(end):
        printed_rows = 13 #increase by every extra print - row

        rows, columns = get_terminal_size()

        if inp.upper() == "E":
            #end = True
            break;  
        front_page()
        
        if message != "":
            printed_rows += 6

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
        valid, message = input_valid(inp)


    print('\n***\nEnding Password Generator.\nMemory has been cleared.\nStay safe and Goodbye.')

def front_page():
    """
    Display front page containing: Settings info, Action options, Status message and Input
    """

    #settings = SHEET.worksheet('settings')
    #data = settings.get_all_values()
    #print(data)

    print("*** Password Generator ***")
    print("")
    print("Settings:")
    print("[L] Password Length: <15>")
    print("[U] Use uppercase: <Yes>")
    print("[O] Use lowercase: <Yes>")
    print("[N] Use Numbers: <No>")
    print("[S] Use special characters: <No>")
    print("")
    print("Generated password: ")
    print("")
    print("[G] Generate Passowrd, [E] End Program")

def input_valid(inp):
    """
    Checks if user input is valid, returns true if it is, if not it will return message
    """
    message = ""

    if inp.upper() in ('L', 'U', 'O', 'N', 'S', 'G', 'E'):
        return True, message
    else:
        return False, "Input value is invalid. \nType in 'L' 'U', 'O', 'N', 'S', 'G', 'E' \nor 'l' 'u', 'o', 'n', 's', 'g', 'e'."



def get_terminal_size():
    import sys
    import subprocess

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            return struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return None

    # Try to get terminal size using os.get_terminal_size() if available
    try:
        import os
        size = os.get_terminal_size()
        return size.lines, size.columns
    except:
        pass

    # Try to get terminal size using ioctl
    for fd in (0, 1, 2):
        sz = ioctl_GWINSZ(fd)
        if sz:
            return sz

    # Try to get terminal size using subprocess and stty
    try:
        sz = subprocess.check_output(['stty', 'size']).split()
        return int(sz[0]), int(sz[1])
    except:
        pass

    # Default size if all methods fail
    return 25, 80  # Default to 25 lines and 80 columns

"""
Start of Password Generator Program
"""
program()
