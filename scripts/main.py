import os
import time
from pyfiglet import Figlet
from rich.console import Console

# Initialize the console from Rich for color
console = Console()

def display_intro(console_width, current_path):
    """Display the introduction, ASCII art, and current path."""
    os.system("cls" if os.name == "nt" else "clear")

    # Generate ASCII art
    fig = Figlet(font="standard")
    ascii_art_lines = fig.renderText("C O D E B A S E").split("\n")

    # Print ASCII art at the top, centered
    for line in ascii_art_lines:
        if line.strip():  # Skip empty lines
            console.print(line.center(console_width), style="bold yellow")

    intro_text = (
        "\n[bold cyan]Welcome to the Codebase Project Setup Tool.[/bold cyan]\n"
        "This tool helps you easily manage and organize your programming projects.\n"
        "Type 'exit' or press 'ctrl c' to quit.\n"
    )
    console.print(intro_text, justify="center")

    # Print the current working directory
    console.print(f"[bold green]{current_path}[/bold green] >>", end=" ")

def main():
    """Main program function."""
    current_width = os.get_terminal_size().columns
    current_path = os.getcwd()

    display_intro(current_width, current_path)



if __name__ == "__main__":
    main()
