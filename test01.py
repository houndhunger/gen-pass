try:
    import pyperclip
    print('I asume pyperclip is installed')
except ImportError:
    print('Something wrong with pyperclip')

pyperclip.copy('The text to be copied to the clipboard.')
print(f"And Paste: {pyperclip.paste()}")