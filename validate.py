import calculations
import sections

import sys  # for sudden exit on unidentified input


def default_inp_message():
    """
    Default Message
    """
    return "Choose next operation: \n"


def build_screen(settings, password, inp_message):
    """
    Building screen from top - header to the bottom input,
    filling the whole screen
    It responds to screen rows count to fill whole screen correctly
    """
    if settings['ACTIVE-OP'] == 'H':
        help_content = sections.help_screen()
        print(help_content)
        rows_c = calculations.count_returns(help_content)
    else:
        rows, columns = calculations.get_terminal_size()
        rows_c = 0  # 1 extra line on input message outside rows_c *
        rows_c += sections.title_section(rows)
        rows_c += sections.legend_and_op_section(settings['ACTIVE-OP'], rows)
        rows_c += sections.settings_section(settings, rows)
        rows_c += sections.sum_section(settings, rows)
        rows_c += sections.password_section(password)
    rows_c += calculations.count_returns(inp_message)

    # blank lines to fill the the screen
    sections.blank_lines_section(rows_c)

    # input message
    try:
        inp_value = input(inp_message).upper()
    except ValueError as e:
        print("Invalid input, something went wrong:", e)
        # Exit the script
        sys.exit(1)
    return inp_value


def screen_and_get_any(
        settings, password, inp_value, inp_message, operation):
    """
    Not so much validation as just returning to home screen
    """
    settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
    _ = build_screen(settings, password, inp_message)
    inp_message = f"\n{default_inp_message()}"
    settings['ACTIVE-OP'] = 'HOME'
    return settings, inp_message


def screen_and_get_max(settings, password, inp_value, inp_message, operation):
    """
    Validation for Maximum value input
    """
    while True:
        settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
        _ = build_screen(settings, password, inp_message)
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
            elif inp_value < settings[operation]['min']:
                inp_message += f"\nMaximum '{inp_value}' "
                inp_message += "cannot be less then Minimum "
                inp_message += f"\'{settings[operation]['min']}'."
                inp_message += "\nPlease enter Maximum count: <"
                inp_message += f"{settings[operation]['max']}> "
        except ValueError:
            if inp_value == '\\' and \
                int(settings[operation]['min']) <= \
                    int(settings[operation]['max']):
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += "\nYou cancelled "
                inp_message += f"{settings[operation]['name']} operation."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '' and \
                int(settings[operation]['min']) <= \
                    int(settings[operation]['max']):
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += "\nYou confirmed previus Maximum value "
                inp_message += f"{settings[operation]['max']}."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '' and \
                int(settings[operation]['max']) < \
                    int(settings[operation]['min']):
                inp_message += f"\nMaximum '{settings[operation]['max']}' "
                inp_message += "cannot be less then Minimum "
                inp_message += f"\'{settings[operation]['min']}'."
                inp_message += "\nPlease enter Maximum count: <"
                inp_message += f"{settings[operation]['max']}> "
            elif inp_value == '\\' and \
                int(settings[operation]['max']) < \
                    int(settings[operation]['min']):
                inp_message += f"\nMaximum '{settings[operation]['max']}' "
                inp_message += "cannot be less then Minimum "
                inp_message += f"\'{settings[operation]['min']}'."
                inp_message += "\nYou went step back. Please enter Minimum "
                inp_message += f"count: <{settings[operation]['min']}> "
                settings, inp_message = screen_and_get_min(
                    settings, password, inp_value, inp_message, operation
                    )
                break
            else:
                inp_message += "\nInvalid value!"
                inp_message += \
                    "\nPlease enter Maximum count between " + \
                    "1 and 4096 and bigger then Minimum: "
    return settings, inp_message


def screen_and_get_min(settings, password, inp_value, inp_message, operation):
    """
    Validation for Minimum value input
    """
    while True:
        settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)
        inp_message = ""
        # Check input
        try:
            inp_value = int(inp_value)
            if inp_value >= 1 and inp_value <= 4096:
                settings[operation]['min'] = inp_value
                inp_message += "\nYou set Minimum count to "
                inp_message += f"{settings[operation]['min']}."
                inp_message += "\nPlease enter Maximum count: <"
                inp_message += f"{settings[operation]['max']}> "
                settings, inp_message = screen_and_get_max(
                    settings, password, inp_value, inp_message, operation
                    )
                break
            else:
                inp_message += f"\nInvalid value <{inp_value}>!"
                inp_message += "\nPlease enter Minimum count (1-4096): <"
                inp_message += f"{settings[operation]['min']}> "
        except ValueError:
            if inp_value == '\\':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += "\nYou cancelled "
                inp_message += f"{settings[operation]['name']} operation."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '':
                inp_message += "\nYou confirmed previous Minimum count "
                inp_message += f"{settings[operation]['min']}."
                inp_message += "\nPlease enter Maximum count: <"
                inp_message += f"{settings[operation]['max']}> "
                settings, inp_message = screen_and_get_max(
                    settings, password, inp_value, inp_message, operation
                    )
                break
            else:
                inp_message += "\nInvalid value!"
                inp_message += "\nPlease enter Minimum count (1-4096): <"
                inp_message += f"{settings[operation]['min']}> "
    return settings, inp_message


def screen_and_get_yes_no(
        settings, password, inp_value, inp_message, operation):
    """
    Validation for Yes/No value input
    """
    while True:
        # build screen
        inp_value = build_screen(settings, password, inp_message)
        inp_message = ""
        # check inupt
        if inp_value == 'Y':
            settings[operation]['value'] = 'Yes'
            inp_message += "\nYou selected 'Yes'."
            inp_message += "\nPlease enter Minimum count: <"
            inp_message += f"{settings[operation]['min']}> "
            settings, inp_message = screen_and_get_min(
                settings, password, inp_value, inp_message, operation
                )
            break
        elif inp_value == 'N':
            settings[operation]['value'] = 'No'
            settings['ACTIVE-OP'] = 'HOME'
            inp_message += "\nYou selected 'No'."
            inp_message += f"\n{default_inp_message()}"
            break
        elif inp_value == '\\':
            settings['ACTIVE-OP'] = 'HOME'
            inp_message += "\nYou cancelled "
            inp_message += f"{settings[operation]['name']} operation."
            inp_message += f"\n{default_inp_message()}"
            break
        elif inp_value == '':
            if settings[operation]['value'] == 'Yes':
                inp_message += "\nYou confirmed previus value 'Yes'."
                inp_message += "\nPlease enter Minimum count: <"
                inp_message += f"{settings[operation]['min']}> "
                settings, inp_message = screen_and_get_min(
                    settings, password, inp_value, inp_message, operation
                    )
                break
            elif settings[operation]['value'] == 'No':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += "\nYou confirmed previus value 'No'."
                inp_message += f"\n{default_inp_message()}"
                break
        else:
            inp_message += "\nInvalid key!"
            inp_message += "\nPlease enter 'Y' for Yes or 'N' for No: <"
            inp_message += f"{settings[operation]['value']}> "
    return settings, inp_message


def screen_and_get_value(
        settings, password, inp_value, inp_message, operation):
    """
    Validation for password count input
    """
    while True:
        # build screen
        inp_value = build_screen(settings, password, inp_message)
        inp_message = ""
        # Check input
        try:
            inp_value = int(inp_value)
            if (inp_value >= 1 and inp_value <= 100):
                settings[operation]['value'] = inp_value
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += "\nYou set generated password count to "
                inp_message += f"{settings[operation]['value']}."
                inp_message += f"\n{default_inp_message()}"
                break
        except ValueError:
            if inp_value == '\\':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += "\nYou cancelled "
                inp_message += f"{settings[operation]['name']} operation."
                inp_message += f"\n{default_inp_message()}"
                break
            elif inp_value == '':
                settings['ACTIVE-OP'] = 'HOME'
                inp_message += "\nYou confirmed generated password count "
                inp_message += f"{settings[operation]['value']}."
                inp_message += f"\n{default_inp_message()}"
                break
            else:
                inp_message += "\nInvalid value!"
                inp_message += "\nPlease enter generated password count "
                inp_message += "between 1 and 100: <"
                inp_message += f"{settings[operation]['value']}> "
    return settings, inp_message


def screen_and_get_operation(settings):
    """
    Primary operation, keeps program looping till the End of Program
    """
    password = ""
    inp_message = default_inp_message()
    inp_value = ""

    while True:
        settings, sum_lmin, sum_lmax = calculations.sum_min_max(settings)
        inp_value = build_screen(settings, password, inp_message)
        status_min, status_max = calculations.check_sum_min_max(settings)
        # Check input
        if inp_value == 'L':
            settings['ACTIVE-OP'] = inp_value
            inp_message = "\n\nPlease enter Minimum count: <"
            inp_message += f"{settings[inp_value]['min']}> "
            settings, inp_message = screen_and_get_min(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value in ('U', 'O', 'N', 'S'):
            settings['ACTIVE-OP'] = inp_value
            inp_message = "\nDo you want to use "
            inp_message += f"{settings[inp_value]['name']}?"
            inp_message += "\nPlease enter 'Y' for Yes or 'N' for No: <"
            inp_message += f"{settings[inp_value]['value']}> "
            settings, inp_message = screen_and_get_yes_no(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'G' and status_min and status_max:
            inp_message = "\nPassword has been generated."
            inp_message += f"\n{default_inp_message()}"
            password = calculations.generate_password(settings)
        elif inp_value == 'G' and not (status_min and status_max):
            inp_message = \
                "\n'!' The '!' symbol in the SUM indicates a problem. " + \
                "Ensure that the sum \nof the minimum values exceeds the " + \
                "maximum password length, and vice versa. \nAdjust the " + \
                "minimum and maximum variables to enable password generation."
        elif inp_value == 'H':
            settings['ACTIVE-OP'] = inp_value
            inp_message = "\nSubmit any key to return to the main screen: "
            settings, inp_message = screen_and_get_any(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'B':
            settings['ACTIVE-OP'] = inp_value
            inp_message += \
                "\n\nHow many passwords you want to generate (1-100)? <"
            inp_message += f"{settings[inp_value]['value']}> "
            settings, inp_message = screen_and_get_value(
                settings, password, inp_value, inp_message, inp_value
                )
        elif inp_value == 'C':
            settings['ACTIVE-OP'] = inp_value
            inp_message = "\nPassword has been copied to the clipboard."
            ##### pyperclip & clipboard
            try:
                pyperclip.copy(password)
            except pyperclip.PyperclipException:
                inp_message += " Clipboard function is not supported."
            inp_message += f"\n{default_inp_message()}"
        elif inp_value == 'R':
            settings['ACTIVE-OP'] = inp_value
            inp_message = "\nPassword has been cleared from the clipboard."
            inp_message += f"\n{default_inp_message()}"
            calculations.clear_clipboard()
        elif inp_value == '':
            pass
        elif inp_value == 'E':
            break
        else:
            inp_message = "Invalid key! Plese Enter the key"
            inp_message += "\neather uppercase 'L', 'U', 'O', 'N', 'S',"
            inp_message += " 'G', 'E'"
            inp_message += "\nor lowercase 'l', 'u', 'o', 'n', 's',"
            inp_message += " 'g', 'e':"
