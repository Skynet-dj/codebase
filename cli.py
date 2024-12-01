import os
import time
from pyfiglet import Figlet
from rich.console import Console
import cookiecutter
#native dependencies


def display_intro(console_width):
    os.system("cls" if os.name == "nt" else "clear")
    # Initialize the console from Rich for color
    console = Console()

    # Generate ASCII art
    fig = Figlet(font="standard")
    ascii_art_lines = fig.renderText("Codebase").split("\n")

    # Print ASCII art at the top, centered
    for line in ascii_art_lines:
        if line.strip():  # Skip empty lines
            console.print(line.center(console_width), style="bold yellow")

    # Introductory text
    intro_text = (
        "\nWelcome to the Codebase Project Setup Tool.\n"
        "This tool helps you easily manage and organize your programming projects.\n"
        "Use it to create, configure, and maintain your project files efficiently.\n"
        "Resize the terminal to see it adjust dynamically. Press Ctrl+C to quit.\n"
    )

    # Print introductory text below the banner
    console.print(intro_text, style="bold cyan", justify="center")

def main():   
    display_intro(os.get_terminal_size().columns)
    current_width = os.get_terminal_size().columns

    try:
        while True:
            # Check if the terminal size has changed
            new_width = os.get_terminal_size().columns
            if new_width != current_width:
                current_width = new_width
                display_intro(current_width)

            # Sleep briefly to reduce CPU usage
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Exit gracefully when Ctrl+C is pressed
        print("\nExiting... Goodbye!")

