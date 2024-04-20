import calculations
import sections

def default_inp_message():
    message = "Choose next operation: "
    return message

def build_screen(settings, password, inp_message):
    """
    building screen from top - header to the bottom  
        - input, filling the whole screen
    It responds to screen rows count to fill
    whole screen correctly  
    """
    if settings['ACTIVE-OP'] == 'H':
        help_content = sections.help_screen()
        print(help_content)
        rows_c = calculations.count_returns(help_content)
    else:
        rows, columns = calculations.get_terminal_size()
        rows_c = 0
        rows_c += sections.title_section(rows)
        rows_c += sections.legend_and_op_section(settings['ACTIVE-OP'], rows)
        rows_c += sections.settings_section(settings, rows)
        rows_c += sections.sum_section(settings, rows)
        rows_c += sections.password_section(password)       
    rows_c += calculations.count_returns(inp_message)

    #blank lines to fill the the screen
    sections.blank_lines_section(rows_c) 

    #input message
    try:
        inp_value = input(f"{inp_message}\n").upper()
    except:
        ##### I need to call here Invalid input and message
        inp_value = 'X'
    return inp_value

def screen_and_get_any(
    settings, password, inp_value, inp_message, operation
    ):
    settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
    inp_value = build_screen(settings, password, inp_message)
    inp_message = f"\n{default_inp_message()}"
    settings['ACTIVE-OP'] = 'HOME'
    return settings, inp_message

def screen_and_get_max(settings, password, inp_value, inp_message, operation):
    while True:
        settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)
        inp_message = ""
        # Check input
        try:
            inp_value = int(inp_value)
            if inp_value >= 1 and inp_value <= 4096 and \
            inp_value >= settings[operation]['min']:
                settings[operation]['max'] = inp_value
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += \
                f"\nYou set Maximum value to {settings[operation]['max']}."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value <= settings[operation]['min']:
                inp_message += f"\nMaximum cannot be less then Minimum "
                inp_message += f"\'{settings[operation]['min']}'."
                inp_message += f"\nPlease enter Maximum count: < "
                inp_message += f"{settings[operation]['max']}> "
        except ValueError:
            if inp_value == '\\' and \
            int(settings[operation]['min']) <= \
            int(settings[operation]['max']):
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += f"\nYou cancelled "
                inp_message += f"{settings[operation]['name']} operation."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '' and \
            int(settings[operation]['min']) <= \
            int(settings[operation]['max']):
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += f"\nYou confirmed previus Maximum value "
                inp_message += f"{settings[operation]['max']}."
                inp_message += f"\n{default_inp_message()}"
                break
            else:
                inp_message += f"\nInvalid value!"
                inp_message += \
                f"\nPlease enter Maximum count between " + \
                "1 and 4096 and bigger then Minimum: "
    return settings, inp_message

def screen_and_get_min(settings, password, inp_value, inp_message, operation):
    while True:
        settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)
        inp_message = ""
        # Check input
        try:
            inp_value = int(inp_value)
            if inp_value >= 1 and inp_value <= 4096:
                settings[operation]['min'] = inp_value
                inp_message += f"\nYou set Minimum count to "
                inp_message += f"{settings[operation]['min']}."
                inp_message += f"\nPlease enter Maximum count: <"
                inp_message += f"{settings[operation]['max']}> "
                settings, inp_message = screen_and_get_max(
                    settings, password, inp_value, inp_message, operation
                    )
                break
            else:
                inp_message += f"\nInvalid value <{inp_value}>!"
                inp_message += f"\nPlease enter Minimum count (1-4096): <"
                inp_message += f"{settings[operation]['min']}> "  
        except ValueError:
            if inp_value == '\\':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += f"\nYou cancelled "
                inp_message += f"{settings[operation]['name']} operation."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '':
                inp_message += f"\nYou confirmed previous Minimum count "
                inp_message += f"{settings[operation]['min']}."
                inp_message += f"\nPlease enter Maximum count: <"
                inp_message += f"{settings[operation]['max']}> "
                settings, inp_message = screen_and_get_max(
                    settings, password, inp_value, inp_message, operation
                    )
                break
            else:
                inp_message += f"\nInvalid value!"
                inp_message += f"\nPlease enter Minimum count (1-4096): <"
                inp_message += f"{settings[operation]['min']}> "
    return settings, inp_message


def screen_and_get_yes_no(
    settings, password, inp_value, inp_message, operation
    ):
    while True:
        #build screen
        inp_value = build_screen(settings, password, inp_message)
        inp_message = ""
        #check inupt
        if inp_value == 'Y':
            settings[operation]['value'] = 'Yes'
            inp_message += f"\nYou selected 'Yes'."
            inp_message += f"\nPlease enter Minimum count: <"
            inp_message += f"{settings[operation]['min']}> "
            settings, inp_message = screen_and_get_min(
                settings, password, inp_value, inp_message, operation
                )
            break
        elif inp_value == 'N':
            settings[operation]['value'] = 'No'
            settings['ACTIVE-OP'] = 'HOME'
            inp_message += f"\nYou selected 'No'."
            inp_message += f"\n{default_inp_message()}"
            break
        elif inp_value == '\\':
            settings['ACTIVE-OP'] = 'HOME'
            inp_message += f"\nYou cancelled "
            inp_message += f"{settings[operation]['name']} operation."
            inp_message += f"\n{default_inp_message()}"
            break
        elif inp_value == '':
            if settings[operation]['value'] == 'Yes':
                inp_message += f"\nYou confirmed previus value 'Yes'."
                inp_message += f"\nPlease enter Minimum count: <"
                inp_message += f"{settings[operation]['min']}> "
                settings, inp_message = screen_and_get_min(
                    settings, password, inp_value, inp_message, operation
                    )
                break 
            elif settings[operation]['value'] == 'No':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += f"\nYou confirmed previus value 'No'."
                inp_message += f"\n{default_inp_message()}"
                break
        else:
            inp_message += f"\nInvalid key!"
            inp_message += f"\nPlease enter 'Y' for Yes or 'N' for No: <"
            inp_message += f"{settings[operation]['value']}> "
            #if inp_value in ('Y', 'N'):
            #    inp_value = operation
    return settings, inp_message


def screen_and_get_value(
    settings, password, inp_value, inp_message, operation
    ):
    while True:
        #build screen
        inp_value = build_screen(settings, password, inp_message)
        inp_message = ""
        # Check input
        try:
            inp_value = int(inp_value)
            if (inp_value >= 1 and inp_value <= 100):
                settings[operation]['value'] = inp_value
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += f"\nYou set generated password count to "
                inp_message += f"{settings[operation]['value']}."
                inp_message += f"\n{default_inp_message()}"
                break
        except ValueError:
            if inp_value == '\\':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += f"\nYou cancelled "
                inp_message += f"{settings[operation]['name']} operation."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += f"\nYou confirmed generated password count "
                inp_message += f"{settings[operation]['value']}."
                inp_message += f"\n{default_inp_message()}"
                break
            else:
                inp_message += f"\nInvalid value!"
                inp_message += f"\nPlease enter generated password count "
                inp_message += f"between 1 and 100: <"
                inp_message += f"{settings[operation]['value']}> "
    return settings, inp_message

def screen_and_get_operation(settings):
    """
    Keeps program looping till the End of Program
    """
    password = ""
    inp_message = default_inp_message()
    inp_value = ""

    while True:
        settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)
        status_min, status_max = calculations.check_sum_min_max(settings)
        print(status_min, status_max)
        # Check input
        if inp_value == 'L':
            settings['ACTIVE-OP'] = inp_value          
            inp_message = f"\n"
            inp_message += f"\nPlease enter Minimum count: <"
            inp_message += f"{settings[inp_value]['min']}> "
            settings, inp_message = screen_and_get_min(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value in ('U', 'O', 'N', 'S'):
            settings['ACTIVE-OP'] = inp_value          
            inp_message = f"\nDo you want to use "
            inp_message += f"{settings[inp_value]['name']}?"
            inp_message += f"\nPlease enter 'Y' for Yes or 'N' for No: <"
            inp_message += f"{settings[inp_value]['value']}> "
            settings, inp_message = screen_and_get_yes_no(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'G' and status_min and status_max:
            inp_message = f"\nPassword has been generated."
            inp_message += f"\n{default_inp_message()}"
            password = calculations.generate_password(settings)
        elif inp_value == 'G' and not(status_min and status_max):
            inp_message = \
            f"\nIf the sum of min values exceed the max password length " + \
            f"\nor the sum of max values fall short of the min password " + \
            f"\nlength, adjust the min and max variables " + \
            f"to generate passwords."
        elif inp_value == 'H':
            settings['ACTIVE-OP'] = inp_value
            inp_message = f"\nSubmit any key to return to the main screen: "
            settings, inp_message = screen_and_get_any(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'B':
            settings['ACTIVE-OP'] = inp_value          
            inp_message = f"\n"
            inp_message += \
            f"\nHow many passwords you want to generate (1-100)? <"
            inp_message += f"{settings[inp_value]['value']}> "
            settings, inp_message = screen_and_get_value(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'C':
            settings['ACTIVE-OP'] = inp_value
            inp_message = f"\nPassword has been copied to the clipboard."
            inp_message += f"\n{default_inp_message()}"
            ##### I can't make it work
            try:
                pyperclip.copy("password")
            except:
                pass
        elif inp_value == 'R':
            settings['ACTIVE-OP'] = inp_value
            inp_message = f"\nPassword has been cleared from the clipboard."
            inp_message += f"\n{default_inp_message()}"
            clear_clipboard()
        elif inp_value == '':
             pass
        elif inp_value == 'E':
            break
        else:
            inp_message = f"Invalid key! Plese Enter the key"
            inp_message += f"\neather uppercase 'L', 'U', 'O', 'N', 'S',"
            inp_message += f" 'G', 'E'"
            inp_message += f"\nor lowercase 'l', 'u', 'o', 'n', 's',"
            inp_message += f" 'g', 'e':"
