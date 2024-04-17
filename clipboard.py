import sys
import subprocess
import ctypes

def copy_to_clipboard(password):
    if sys.platform == 'win32':
        # Windows
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.SetClipboardData(1, ctypes.c_wchar_p(password))
        ctypes.windll.user32.CloseClipboard()
    elif sys.platform == 'darwin':
        # macOS
        subprocess.run("pbcopy", universal_newlines=True, input=password)
    elif sys.platform.startswith('linux'):
        # Linux
        try:
            subprocess.run("xclip", universal_newlines=True, input=password)
        except FileNotFoundError:
            # If xclip is not available, try using xsel
            try:
                subprocess.run("xsel", universal_newlines=True, input=password)
            except FileNotFoundError:
                print("Neither xclip nor xsel found. Clipboard interaction not possible.")
    else:
        raise OSError("Clipboard interaction not supported on this platform")


def clear_clipboard():
    if sys.platform == 'win32':
        # Windows
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.CloseClipboard()
    elif sys.platform == 'darwin':
        # macOS
        subprocess.run(["pbcopy"], universal_newlines=True, input="")
    elif sys.platform.startswith('linux'):
        # Linux
        subprocess.run(["xclip", "-selection", "clipboard"], universal_newlines=True, input="")
    else:
        raise OSError("Clipboard interaction not supported on this platform")

