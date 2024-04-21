import calculations

def title_section(rows): 
    """
    It shows if terminal rows >= 26
    """ 
    if rows >= 26:
        print("*** Password Generator ***")
        print("")
    else:
        pass
    return 2

def help_screen():

    with open('help.txt', 'r') as file:
        help_content = file.read()
    return help_content

def legend_and_op_section(active_operation, rows):  
    content = ""
    if rows >= 25:
        content = f"* Legend *\n[] Key   <> Variable"
        content += f"   [-] <-> Not available   ! wrong variables \n" 
        content += f"\n* Operations *\n"
    else:
        content = f"Legend: [] Key   <> Variable   [-] <-> Not available\n"  
        content += f"Operations: " 

    if active_operation == 'HOME':
        content += "[G] Generate Password   "
        content += "[E] End Program   [H] Help"
    else:
        content += "[Enter] Skip   [\] Cancel"
    
    if calculations.is_xsel_installed() or calculations.is_pyperclip_installed():
            content += "   Clipboard: [C] Copy   [R] Clear"    

    print(content)
    return calculations.count_returns(content)

def settings_section(settings, rows):
    """
    It shows settings section table containing 
    relevant operation keys and variable values.
    """
    content = ""
    
    #for terminal row smaller then 21 and 22 to mainitain screen integrity
    if rows > 26:
        content += "\n* Settings *"
   
    keys = ['L', 'B', 'U', 'O', 'N', 'S']
    for i in range(len(keys)):
        if settings['ACTIVE-OP'] != keys[i] and settings['ACTIVE-OP'] != 'HOME':
            keys[i] = '-'
        elif settings['ACTIVE-OP'] != keys[i] and settings['ACTIVE-OP'] != 'HOME':
            keys[i] = 'ACTIVE'

    # Format the settings as a list of lists for tabulate
    settings_table = [
    [f"[{keys[0]}]", settings['L']['name'], "-", 
    f"<{settings['L']['min']}>", f"<{settings['L']['max']}>"],
       
    [f"[{keys[1]}]", settings['B']['name'],"-", f"<{settings['B']['value']}>",
    f"<{settings['B']['value']}>"]
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

    header = ['Operation key:', 'Operation:', 'Yes/No:', 'Min:   ', 'Max:   ']
    content += f"\n{calculations.tabulate(settings_table, headers = header)}"
    
    print(content)
    return calculations.count_returns(content)

def sum_section(settings, rows):
    """
    It shows SUM section - row 
    """
    content = ""
    #for terminal row smaller then 23 to mainitain screen integrity
    if rows >= 23:
        content += "\n"
    content += "SUM of Minimum and Maximum (<Yes> only):      "
    
    status_min, status_max = calculations.check_sum_min_max(settings)
    min_mark = ""
    max_mark = ""
    if not(status_min):
        min_mark = "!"
    if not(status_max):
        max_mark = "!"    
    content += f" Min. {min_mark}{settings['SUM']['min']}    "
    content += f"Max. {max_mark}{settings['SUM']['max']}"

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
    It fills terminal with blank lines to achieve fullscreen effect
    """
    #get terminal size, columns are not used, but prepared for future use
    rows, columns = calculations.get_terminal_size() 
    #blank lines to fill the the screen
    for i in (range(rows - rows_count)):
        print("")