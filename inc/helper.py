# Define the colors using ANSI escape codes

class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'

    RESET = '\033[0m'  # Reset color


def print_color(text, color):
    print(f'{color}{text}{Color.RESET}')
