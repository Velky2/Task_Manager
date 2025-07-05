"""Módulo para utilidades do terminal."""

import os

def clear_screen() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def bold(text: str) -> str:
    return "\033[1m" + text + "\033[22m"


def italic(text: str) -> str:
    return "\033[3m" + text + "\033[23m"


def underline(text: str) -> str:
    return "\033[4m" + text + "\033[24m"


def blinking(text: str) -> str:
    return "\033[5m" + text + "\033[25m"


def inverse(text: str) -> str:
    return "\033[7m" + text + "\033[27m"


def hidden(text: str) -> str:
    return "\033[8m" + text + "\033[28m"


def strikethrough(text: str) -> str:
    return "\033[9m" + text + "\033[29m"
