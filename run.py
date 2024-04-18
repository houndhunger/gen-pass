################################################################################
# Write your code to expect a terminal of 80 characters wide and 24 rows high

def default_inp_message():
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
        length_max = settings['L']['max']

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

def count_returns(string):
    return string.count("\n") + 1

def print_and_count(string):
    print(string)
    return count_returns(string)

def title_section(rows): 
    """
    Displayed Title if terminal rows >= 26
    """ 
    if rows >= 26:
        print("*** Password Generator ***")
        print("")
        #####display['title'] = True
    else:
        pass
        #####display['title'] = False
    return 2

def legend_and_actions_section(active_action, rows):
    
    content = ""
    if rows >= 25:
        content = "* Legend *\n[] Key   <> Variable   [-] <-> Not available\n" 
        content += "\n* Actions *\n"
    else:
        content = "Legend: [] Key   <> Variable   [-] <-> Not available\n"  
        content += "Actions: " 

    if active_action == 'HOME':
        content += "[G] Generate Password   "
        content += "[E] End Program"
    else:
        content += "[Enter] Skip   [\] Cancel"
    
    ##### Kee it until tutoring service is back and helps me with pyperclip   
    """
        if is_xsel_installed() or is_pyperclip_installed():
            string += "[C] Copy to clipboard   [R] Clear clipboard   "    
    """
    print(content)
    return count_returns(content)

################################################################################
def settings_section(settings, rows):
    """
    Display Settings section table containing 
     relevant action keys and variable values.
    """

    content = ""
    #for terminal row smaller then 26 to mainitain screen integrity
    #rows, columns = get_terminal_size()
    #if rows > 26:
    content += "\n* Settings *"
   
   
    aa = settings['ACTIVE-ACTION']
    keys = ['L', 'B', 'U', 'O', 'N', 'S']
    for i in range(len(keys)):
        if aa != keys[i] and settings['ACTIVE-ACTION'] != 'HOME':
            keys[i] = '-'
        elif aa != keys[i] and settings['ACTIVE-ACTION'] != 'HOME':
            keys[i] = 'ACTIVE'


    # Format the settings as a list of lists for tabulate
    settings_table = [
    [f"[{keys[0]}]", settings['L']['name'], "-", 
    f"<{settings['L']['min']}>", f"<{settings['L']['max']}>"],
       
    [f"[{keys[1]}]", settings['B']['name'], f"<{settings['B']['value']}>",
    "-", "-"]
    ]

    short_keys = ('U', 'O', 'N', 'S')
    c = 2
    for key in short_keys:
        settings_table.append([f"[{keys[c]}]", settings[key]['name'],
        f"<{settings[key]['value']}>" if key != 'B' else f"<{settings[key]['value']}>",
        f"<{settings[key]['min'] if settings[key]['value'] != 'No' else '-'}>",
        f"<{settings[key]['max'] if settings[key]['value'] != 'No' else '-'}>"
        ]) 
        c += 1

    #for terminal row smaller then 21 and 22 to mainitain screen integrity
    if rows >= 21:
        settings_table.insert(0, ["---"] * 5)
    if rows >= 22:
        settings_table.insert(3, ["---"] * 5)

    content += f"\n{tabulate(settings_table, headers = [
        'Action key:', 'Action:', 'Yes/No:', 'Min:  ', 'Max:  '
        ])}"
    
    print(content)
    return count_returns(content)

def check_sum_min_max(settings):
    if settings['SUM']['min'] <= settings['L']['max']:
        status_min = True
    else:
        status_min = False
    if settings['SUM']['max'] >= settings['L']['min']:
        status_max = True
    else:
        status_max = False

    return status_min, status_max

def sum_section(settings, rows):
    #for terminal row smaller then 23 to mainitain screen integrity
    content = ""
    if rows >= 23:
        content += "\n"
    content += "SUM of Minimum and Maximum (<Yes> only):  "
    
    status_min, status_max = check_sum_min_max(settings)
    
    if not(status_min):
        sum_min = "!" + sum_min
    if not(status_max):
        sum_max = "!" + sum_max   
    content += f"  Min. {settings['SUM']['min']}, Max. {settings['SUM']['max']}"

    print(content)
    return count_returns(content)

def password_section(password):
    print("")
    print(f"* Generated password{'s' if count_returns(password) > 1 else ''} *")
    print(password) 
    return count_returns(password) + 2

def blank_lines_section(rows_count):
    #get terminal size
    rows, columns = get_terminal_size() 
    #columns - I might not need them, except for "print string width" check...
    #blank lines to fill the the screen
    for i in (range(rows - rows_count)):
        print("")

def build_screen(settings, password, inp_message):
    """
    building screen from top - header to the bottom  
        - input, filling the whole screen
    It responds to screen rows count to fill
    whole screen correctly  
    """
    rows, columns = get_terminal_size()
    rows_count = 0 #increase by every extra print - row
    rows_count += title_section(rows) # 2 lins
    rows_count += legend_and_actions_section(settings['ACTIVE-ACTION'], rows) # 4 lines
    rows_count += settings_section(settings, rows) # 10 lines
    rows_count += sum_section(settings, rows) # 2 lines
    rows_count += password_section(password) # 2+ lines
    rows_count += count_returns(inp_message) # 1 / 4 lines

    #blank lines to fill the the screen
    blank_lines_section(rows_count) 

    #input message
    try:
        inp_value = input(inp_message).upper()
    except:
        # I need to call here Invalid input and message
        inp_value = 'X'
    return inp_value

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

def input_valid(inp_value):
################################################################################
    """
    Checks if user input is valid.
    Returns true if it is, if not it will return message
    """

    if inp_value in ('L', 'U', 'O', 'N', 'S', 'G', 'E'):
        return True, ""
    else: ##### is this used? because input varries
        message = ("Input value is invalid. \n"
        "Type in 'L' 'U', 'O', 'N', 'S', 'G', 'E' \n"
        "or 'l' 'u', 'o', 'n', 's', 'g', 'e'.")
        return False, message

def screen_and_get_max(settings, password, inp_value, inp_message, action):
    while True:
        settings, sum_lmin, sum_lmax = sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)

        # Check input
        try:
            inp_value = int(inp_value)
            if (inp_value >= 1 and inp_value <= 1024) and \
            (inp_value >= settings[action]['min']):
                settings[action]['max'] = inp_value
                settings['ACTIVE-ACTION'] = 'HOME'
                ##### inp_message = action_section(settings[action])
                inp_message += \
                f"\nYou set Maximum value to {settings[action]['max']}."
                inp_message += f"\n{default_inp_message()}"
                break
        except ValueError:
            if inp_value == '\\' and \
            int(settings[action]['min']) <= int(settings[action]['max']):
                settings['ACTIVE-ACTION'] = 'HOME'
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou cancelled \
                {settings[action]['name']} action."
                inp_message += f"\n{default_inp_message()}"
                break
            elif int(settings[action]['min']) > int(settings[action]['max']):
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nMinimum cannot be more then Maximum."
                inp_message += f"\nPlease enter Maximum count: < \
                {settings[action]['max']}> "
            elif inp_value == '':
                settings['ACTIVE-ACTION'] = 'HOME'
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou confirmed previus Maximum value \
                {settings[action]['max']}."
                inp_message += f"\n{default_inp_message()}"
                break
            else:
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nInvalid value!"
                inp_message += f"\nPlease enter Maximum count between \
                1 and 1024 and bigger then Minimum: "
    return settings, inp_message
################################################################################
def screen_and_get_min(settings, password, inp_value, inp_message, action):
    while True:
        settings, sum_lmin, sum_lmax = sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)

        # Check input
        try:
            inp_value = int(inp_value)
            if inp_value >= 1 and inp_value <= 1024:
                settings[action]['min'] = inp_value
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou set Minimum count to \
                {settings[action]['min']}."
                inp_message += f"\nPlease enter Maximum count: <\
                {settings[action]['max']}> "
                settings, inp_message = screen_and_get_max(
                    settings, password, inp_value, inp_message, action
                    )
                break
            else:
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nInvalid value <{inp_value}>!"
                inp_message += f"\nPlease enter Minimum count (1-1024): <\
                {settings[action]['min']}> "  
        except ValueError:
            if inp_value == '\\':
                settings['ACTIVE-ACTION'] = 'HOME'
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou cancelled \
                {settings[action]['name']} action."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '':
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou confirmed previous Minimum count \
                {settings[action]['min']}."
                inp_message += f"\nPlease enter Maximum count: <\
                {settings[action]['max']}> "
                settings, inp_message = screen_and_get_max(
                    settings, password, inp_value, inp_message, action
                    )
                break
            else:
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nInvalid value!"
                inp_message += f"\nPlease enter Minimum count (1-1024): <\
                {settings[action]['min']}> "
    return settings, inp_message

################################################################################
def screen_and_get_yes_no(settings, password, inp_value, inp_message, action):
    while True:
        #build screen
        inp_value = build_screen(settings, password, inp_message)

        #check inupt
        if inp_value == 'Y':
            settings[action]['value'] = 'Yes'
            ##### inp_message = action_section(settings[action])
            inp_message += f"\nYou selected 'Yes'."
            inp_message += f"\nPlease enter Minimum count: <\
            {settings[action]['min']}> "
            settings, inp_message = screen_and_get_min(
                settings, password, inp_value, inp_message, action
                )
            break
        elif inp_value == 'N':
            settings[action]['value'] = 'No'
            settings['ACTIVE-ACTION'] = 'HOME'
            ###### inp_message = action_section(settings[action])
            inp_message += f"\nYou selected 'No'."
            inp_message += f"\n{default_inp_message()}"
            break
        elif inp_value == '\\':
            settings['ACTIVE-ACTION'] = 'HOME'
            ##### inp_message = action_section(settings[action])
            inp_message += f"\nYou cancelled {settings[action]['name']} action."
            inp_message += f"\n{default_inp_message()}"
            break
        elif inp_value == '':
            if settings[action]['value'] == 'Yes':
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou confirmed previus value 'Yes'."
                inp_message += f"\nPlease enter Minimum count: <\
                {settings[action]['min']}> "
                settings, inp_message = screen_and_get_min(
                    settings, password, inp_value, inp_message, action
                    )
                break 
            elif settings[action]['value'] == 'No':
                settings['ACTIVE-ACTION'] = 'HOME'
                ###### inp_message = action_section(settings[action])
                inp_message += f"\nYou confirmed previus value 'No'."
                inp_message += f"\n{default_inp_message()}"
                break
        else:
            ##### inp_message = action_section(settings[action])
            inp_message += f"\nInvalid key!"
            inp_message += f"\nPlease enter 'Y' for Yes or 'N' for No: <\
            {settings[action]['value']}> "
            #if inp_value in ('Y', 'N'):
            #    inp_value = action
    return settings, inp_message

################################################################################
def screen_and_get_value(settings, password, inp_value, inp_message, action):
    while True:
        #build screen
        inp_value = build_screen(settings, password, inp_message)
        
        # Check input
        try:
            inp_value = int(inp_value)
            if (inp_value >= 1 or inp_value <= 100):
                settings[action]['value'] = inp_value
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou set generated password count to \
                {settings[action]['value']}."
                inp_message += f"\n{default_inp_message()}"
                break
        except ValueError:
            if inp_value == '\\':
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou cancelled \
                {settings[action]['name']} action."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '':
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nYou confirmed generated password count \
                {settings[action]['value']}."
                inp_message += f"\n{default_inp_message()}"
                break
            else:
                ##### inp_message = action_section(settings[action])
                inp_message += f"\nInvalid value!"
                inp_message += f"\nPlease enter generated password count \
                between 1 and 100: <{settings[action]['value']}> "
    return settings, inp_message

def screen_and_get_action(settings):
    """
    Keeps program looping till the End of Program
    """
    password = ""
    inp_message = default_inp_message()
    inp_value = ""

    while True:
        settings, sum_lmin, sum_lmax = sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)

        # Check input
        if inp_value == 'L':
            settings['ACTIVE-ACTION'] = inp_value
            inp_message = action_section(settings[inp_value])  
            inp_message += f"\n"
            inp_message += f"\nPlease enter Minimum count: <\
            {settings[inp_value]['min']}> "
            settings, inp_message = screen_and_get_min(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value in ('U', 'O', 'N', 'S'):
            settings['ACTIVE-ACTION'] = inp_value
            inp_message = action_section(settings[inp_value])  
            inp_message += f"\nDo you want to use {settings[inp_value]['name']}?"
            inp_message += f"\nPlease enter 'Y' for Yes or 'N' for No: <\
            {settings[inp_value]['value']}> "
            settings, inp_message = screen_and_get_yes_no(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'G':
            settings['ACTIVE-ACTION'] = inp_value
            inp_message = f"\nPassword has been generated."
            inp_message += f"\n{default_inp_message()}"
            password = generate_password(settings)
        elif inp_value == 'B':
            settings['ACTIVE-ACTION'] = inp_value
            inp_message = action_section(settings[inp_value])  
            inp_message += f"\n"
            inp_message += f"\nHow many passwords you want to generate \
            (1-100)? <{settings[inp_value]['value']}> "
            settings, inp_message = screen_and_get_value(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'C':
            settings['ACTIVE-ACTION'] = inp_value
            inp_message = f"\nPassword has been copied to the clipboard."
            inp_message += f"\n{default_inp_message()}"
            ##### I can't make it work
            try:
                pyperclip.copy("password")
            except:
                pass
        elif inp_value == 'R':
            settings['ACTIVE-ACTION'] = inp_value
            inp_message = f"\nPassword has been cleared from the clipboard."
            inp_message += f"\n{default_inp_message()}"
            clear_clipboard()
        elif inp_value == '':
             pass
        elif inp_value == 'E':
            break
        else:
            inp_message = f"Invalid key! Plese Enter the key"
            inp_message += f"\neather uppercase 'L', 'U', 'O', 'N', 'S', 'G', 'E'"
            inp_message += f"\nor lowercase 'l', 'u', 'o', 'n', 's', 'g', 'e':"
################################################################################



def end():
        print("\n*** \nEnding Password Generator. "
        "\nMemory has been cleared. \nStay safe and Goodbye.")

################################################################################
def main():
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
    # Sum   
    'SUM': {'name': 'SUM', 'min': 0, 'max': 0},
    # Show or not parts of page
    'SHOW': {'settings': True, 'action': False},
    'ACTIVE-ACTION': 'HOME'
    }

    display = {
    'title': False, 
    'actions': False, 'compact_actions': True,
    'primary_actions': True, 'secondary_actions': False,
    'settings': False, 'compact_settings': True,
    'sum': True,
    'password': True,
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
