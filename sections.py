import calculations

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

def help_screen():
    with open('help.txt', 'r') as file:
        help_content = file.read()
    return help_content

def legend_and_op_section(active_operation, rows):  
    content = ""
    if rows >= 25:
        content = "* Legend *\n[] Key   <> Variable"+\
        "   [-] <-> Not available   ! wrong variables \n" 
        content += "\n* Operations *\n"
    else:
        content = "Legend: [] Key   <> Variable   [-] <-> Not available\n"  
        content += "Operations: " 

    if active_operation == 'HOME':
        content += "[G] Generate Password   "
        content += "[E] End Program   [H] Help"
    else:
        content += "[Enter] Skip   [\] Cancel"
    
    ##### Kee it until tutoring service is back and helps me with pyperclip   
    """
        if is_xsel_installed() or is_pyperclip_installed():
            string += "[C] Copy to clipboard   [R] Clear clipboard   "    
    """
    print(content)
    return calculations.count_returns(content)

def settings_section(settings, rows):
    """
    Display Settings section table containing 
     relevant operation keys and variable values.
    """

    content = ""
    #for terminal row smaller then 26 to mainitain screen integrity
    #rows, columns = get_terminal_size()
    #if rows > 26:
    content += "\n* Settings *"
   
   
    aa = settings['ACTIVE-OP']
    keys = ['L', 'B', 'U', 'O', 'N', 'S']
    for i in range(len(keys)):
        if aa != keys[i] and settings['ACTIVE-OP'] != 'HOME':
            keys[i] = '-'
        elif aa != keys[i] and settings['ACTIVE-OP'] != 'HOME':
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

    content += f"\n{calculations.tabulate(settings_table, headers =
    ['Operation key:', 'Operation:', 'Yes/No:', 'Min:   ', 'Max:   '])}"
    
    print(content)
    return calculations.count_returns(content)

def sum_section(settings, rows):
    #for terminal row smaller then 23 to mainitain screen integrity
    content = ""
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
    content += f" Min. {\
    min_mark}{settings['SUM']['min']}    Max. {\
    max_mark}{settings['SUM']['max']}"

    print(content)
    return calculations.count_returns(content)

def password_section(password):
    print("")
    print(f"* Generated password{'s' 
    if calculations.count_returns(password) > 1 else ''} *")
    print(password) 
    return calculations.count_returns(password) + 2

def blank_lines_section(rows_count):
    #get terminal size
    rows, columns = calculations.get_terminal_size() 
    #columns - I might not need them, except for "print string width" check...
    #blank lines to fill the the screen
    for i in (range(rows - rows_count)):
        print("")