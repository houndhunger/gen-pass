import subprocess
import platform
def is_xsel_installed():
    """
    checks if xsel is installed for clclipboard op
    """
    if platform.system() != 'Linux':
        return False  # xsel is only available on Linux
    try:
        subprocess.run(["xsel", "--version"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_pyperclip_installed():
    """
    checks if pyperclip is installed for clclipboard op
    """
    try:
        import pyperclip
        return True
    except ImportError:
        return False

def check_sum_min_max(settings):
    """
    Checks 'SUM min' <= 'password length max' and vice versa
    """
    if settings['SUM']['min'] <= settings['L']['max']:
        status_min = True
    else:
        status_min = False
    if settings['SUM']['max'] >= settings['L']['min']:
        status_max = True
    else:
        status_max = False
    return status_min, status_max

def sum_min_max(settings):
    """
    SUMarize active Minimal and Maximal values
    """
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

import os
def get_terminal_size():
    """
    Gets terminal size - rows, columns(future use)
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

def count_returns(string):
    """
    Count returns
    """
    return string.count("\n") + 1

def print_and_count(string):
    """
    Printe and count returns
    """
    print(string)
    return count_returns(string)

def tabulate(table, headers):
    """
    Tabulate - draw a table from array data and returns it as a string
    """
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
            str(cell).ljust(column_widths[i], "-") 
            if cell == "---" 
            else str(cell).ljust(column_widths[i]) for i, cell in enumerate(row)
            ]
        formatted_table.append(formatted_row)

    table = ""
    # Print the formatted table
    for row in formatted_table:
        table +=" | ".join(row) + "\n"
    
    return table[:-1]

import random
import string
def generate_password(settings):
    """
    Generates password as string or passwords as multiline string
    """
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
        length_max = settings['L']['max']

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