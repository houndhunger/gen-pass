"""
This module provides functions for displaying various sections of the password
generator interface.

Importing this module allows access to functions for displaying the title
section, help screen, legend and operations section, settings section, SUM
section, password section and blank lines section.

Module Functions:
    - title_section(rows): Displays the title section of the password
    generator interface.
    - help_screen(): Displays the help screen.
    - legend_and_op_section(active_operation, rows): Displays the legend
    and operations section.
    - settings_section(settings, rows): Displays the settings section.
    - sum_section(settings, rows): Displays the SUM section.
    - password_section(password): Displays the settings section, which
    includes a table containing relevant operation keys and their
    corresponding variable values.
    - blank_lines_section(rows_count): Fills the terminal with blank lines
    to achieve fullscreen effect.
"""

import calculations


def title_section(rows):
    """
    Displays the title section of the password generator interface.
    """
    if rows >= 26:
        print("*** Password Generator ***")
        print("")
    else:
        pass
    return 2


def help_screen():
    """
    Displays the help screen.
    """
    with open('help.txt', 'r', encoding='utf-8') as file:
        help_content = file.read()
    return help_content


def legend_and_op_section(active_operation, rows):
    """
    Displays the legend and operations section.
    """
    content = ""
    if rows >= 25:
        content = "* Legend *\n[] Key   <> Variable"
        content += "   [-] <-> Not available   ! wrong values \n"
        content += "\n* Operations *\n"
    else:
        content = "Legend: [] Key   <> Variable   [-] <-> Not available\n"
        content += "Operations: "

    if active_operation == 'HOME':
        content += "[G] Generate Password   "
        content += "[E] End Program   [H] Help"
    else:
        content += "[Enter] Skip   [\\] Cancel"

    print(content)
    return calculations.count_returns(content)


def settings_section(settings, rows):
    """
    Displays the settings section, which includes a table containing relevant
    operation keys and their corresponding variable values.
    """
    content = ""

    # for terminal row smaller then 21 and 22 to mainitain screen integrity
    if rows > 26:
        content += "\n* Settings *"

    keys = ['L', 'B', 'U', 'O', 'N', 'S']

    # show keys or not depending if ACTIVE-OP is primary operation
    for i, key in enumerate(keys):
        if (
            settings['ACTIVE-OP'] != key and
            settings['ACTIVE-OP'] != 'HOME'
        ):
            keys[i] = '-'
        elif (
            settings['ACTIVE-OP'] != key and
            settings['ACTIVE-OP'] != 'HOME'
        ):
            keys[i] = 'ACTIVE'

    # Mark wrong values with '!'
    status_min, status_max = calculations.check_sum_min_max(settings)
    min_m = ""
    max_m = ""

    min_m = "!" if not status_min else ""
    max_m = "!" if not status_max else ""

    # format the settings as a list of lists for tabulate
    settings_table = [
        [
            f"[{keys[0]}]", settings['L']['name'], "-",
            f"{max_m}<{settings['L']['min']}>",
            f"{min_m}<{settings['L']['max']}>"
        ],

        [
            f"[{keys[1]}]", settings['B']['name'], "-",
            f"<{settings['B']['value']}>",
            f"<{settings['B']['value']}>"
        ]
    ]

    short_keys = ('U', 'O', 'N', 'S')
    c = 2  # count set to 2, as keys[0] and keys[1] already parsed
    for key in short_keys:
        if settings[key]['value'] != 'No':
            yn_min = settings[key]['min']
        else:
            yn_min = '-'
        if settings[key]['value'] != 'No':
            yn_max = settings[key]['max']
        else:
            yn_max = '-'
        settings_table.append([
            f"[{keys[c]}]", settings[key]['name'],
            f"<{settings[key]['value']}>"
            if key != 'B' else f"<{settings[key]['value']}>",
            f"{min_m}<{yn_min}>",
            f"{max_m}<{yn_max}>"
        ])
        c += 1

    # for terminal row smaller then 21 and 22 to mainitain screen integrity
    if rows >= 21:
        settings_table.insert(0, ["---"] * 5)
    if rows >= 22:
        settings_table.insert(3, ["---"] * 5)

    header = ['Operation key:', 'Operation:', 'Yes/No:', 'Min:   ', 'Max:   ']
    content += f"\n{calculations.tabulate(settings_table, headers=header)}"

    print(content)
    return calculations.count_returns(content)


def sum_section(settings, rows):
    """
    Displays the SUM section.
    """
    content = ""
    # for terminal row smaller then 23 to mainitain screen integrity
    if rows >= 23:
        content += "\n"
    content += "SUM of Minimum and Maximum (<Yes> only):      "

    status_min, status_max = calculations.check_sum_min_max(settings)
    content += f" Min. {'!' if not status_min else ''}"
    content += f"{settings['SUM']['min']}    "
    content += f"Max. {'!' if not status_max else ''}"
    content += f"{settings['SUM']['max']}"

    print(content)
    return calculations.count_returns(content)


def password_section(password):
    """
    It shows password section
    """
    print("")
    password_plural = 's' if calculations.count_returns(password) > 1 else ''
    gen_pass_title = f"* Generated password{password_plural} *"
    print(gen_pass_title)
    print(password)
    return calculations.count_returns(password) + 2


def blank_lines_section(rows_count):
    """
    Fills the terminal with blank lines to achieve fullscreen effect.
    """
    # get terminal size, columns are not used, but prepared for future use
    rows, _ = calculations.get_terminal_size()
    # blank lines to fill the the screen
    print("\n".join(["" for _ in range(rows - rows_count)]))
