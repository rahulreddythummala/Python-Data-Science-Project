import os
from sys import stdout

def clear():
    #os.system('cls' if os.name == 'nt' else 'clear')
    if stdout.isatty():
        os.system('cls')
    else:
        os.system('clear')
        