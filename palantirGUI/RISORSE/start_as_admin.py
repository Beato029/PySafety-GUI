import os
import sys
import ctypes

# Aggiungi questa funzione per gestire i permessi
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()

if not is_admin():
    # Riavvia come amministratore su Windows
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)