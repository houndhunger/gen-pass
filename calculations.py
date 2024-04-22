"""
A module for generating passwords and performing related calculations.

Includes functions to check the validity of password length settings,
summarize active minimal and maximal values, retrieve terminal size,
count return characters in a string, print and count return characters,
tabulate data into a formatted table, generate passwords, and perform testing.

Functions:
    - check_sum_min_max(settings): Checks if 'SUM min' <= 'password length max' and vice versa.
    - sum_min_max(settings): Summarizes active minimal and maximal values.
    - get_terminal_size(): Retrieves the terminal size.
    - count_returns(string): Counts return characters in a string.
    - print_and_count(string): Prints a string and counts return characters.
    - tabulate(table, headers): Draws a table from array data and returns it as a string.
    - generate_password(settings): Generates passwords as a string or multiline string.

"""
# required for generate_password()
import random
import string

# required for get_terminal_size()
import os



def check_sum_min_max(settings):
    """
    Checks if 'SUM min' <= 'password length max' and vice versa.
    """
    status_min = settings['SUM']['min'] <= settings['L']['max']
    status_max = settings['SUM']['max'] >= settings['L']['min']
    return status_min, status_max


def sum_min_max(settings):
    """
    Summarizes active minimal and maximal values.
    """
    char_type = ('U', 'O', 'N', 'S')
    sum_lmin = 0
    sum_lmax = 0
    for ch in char_type:
        if settings[ch]['value'] == 'Yes':
            sum_lmin += settings[ch]['min']
            sum_lmax += settings[ch]['max']
    settings['SUM']['min'] = sum_lmin
    settings['SUM']['max'] = sum_lmax
    return settings, sum_lmin, sum_lmax


def get_terminal_size():
    """
    Retrieves the terminal size.
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)


def count_returns(input_string):
    """
    Counts return characters in a string.
    """
    return input_string.count("\n") + 1


def print_and_count(input_string):
    """
    Prints a string and counts return characters.
    """
    print(input_string)
    return count_returns(input_string)


def tabulate(table, headers):
    """
    Draws a table from array data and returns it as a string.
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
            else str(cell).ljust(column_widths[i])
            for i, cell in enumerate(row)
            ]
        formatted_table.append(formatted_row)

    table = ""
    # Print the formatted table
    for row in formatted_table:
        table += " | ".join(row) + "\n"

    return table[:-1]


def generate_password(settings):
    """
    Generates passwords as a string or multiline string.
    """
    settings, sum_lmin, sum_lmax = sum_min_max(settings)

    if sum_lmin > settings['L']['min']:
        length_min = sum_lmin
    else:
        length_min = settings['L']['min']
    if sum_lmax > settings['L']['max']:
        length_max = sum_lmax
    else:
        length_max = settings['L']['max']

    char_type = ('U', 'O', 'N', 'S')
    ps_comp = {
        'U': string.ascii_letters.upper(), 'O': string.ascii_letters.lower(),
        'N': string.digits, 'S': string.punctuation
        }

    passwords = ""

    for _ in range(settings['B']['value']):
        password = ""
        # Generate password components
        for ch in char_type:
            if settings[ch]["value"] == 'Yes':
                password += ''.join(random.choices(
                    ps_comp[ch], k=settings[ch]['min']
                    ))

        password_length = random.randint(length_min, length_max)

        # Get character types with 'Yes' values in settings
        yes_char_types = [
            ch for ch in char_type
            if settings[ch]["value"] == 'Yes'
            ]

        # Fill the remaining length with random characters
        if password_length - sum_lmin > 0:
            remaining_characters = ''.join(
                random.choices(
                    ''.join(ps_comp[ch] for ch in yes_char_types),
                    k = password_length - sum_lmin
                )
            )
            password += remaining_characters

        # Shuffle the password to ensure randomness
        random.shuffle(list(password))
        password = ''.join(list(password))
        passwords += password + "\n"

    return passwords
