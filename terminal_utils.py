import os

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def bold(text: str) -> str:
    return "\033[1m" + text + "\033[0m"