import os
from rich.console import Console
from pyfiglet import Figlet

def display_ascii():
    # Clear the screen (works for both Windows and Linux/macOS)
    os.system("cls" if os.name == "nt" else "clear")

    # Initialize the console from Rich
    console = Console()

    # Generate ASCII art using PyFiglet
    fig = Figlet(font='standard')
    ascii_art = fig.renderText("Codebase")

    # Display the ASCII art with color using Rich
    console.print(ascii_art, style="bold yellow")

if __name__ == "__main__":
    display_ascii()
