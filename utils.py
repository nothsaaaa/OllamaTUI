import pyfiglet
import random
from termcolor import colored

def blank(num):
    print('\n' * num)

def figlet(text):
    def random_color(text):
        colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        return colored(text, random.choice(colors))

    ascii_art = pyfiglet.figlet_format(text)

    for line in ascii_art.splitlines():
        print(random_color(line))

def clear_screen():
    print("\n" * 100)

