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
    inp = input("Choose action: ")

front_page()
