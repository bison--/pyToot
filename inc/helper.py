import shutil

# Define the colors using ANSI escape codes
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'

    BLUE = '\033[94m'

    RESET = '\033[0m'  # Reset color


def print_color(text, color):
    print(f'{color}{text}{Color.RESET}')


def get_terminal_width():
    terminal_width = shutil.get_terminal_size().columns
    return terminal_width
