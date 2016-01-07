from termcolor.termcolor import colored
from colorama.colorama import init

init()

def print_colored(message, color):
    print(colored(message, color))