import os
import time
from pyfiglet import Figlet
import pyfiglet
from rich.console import Console
import json

CONFIG_FILE = "data/config.json"
COMMANDS = "data/commands.json"
# Initialize the console from Rich for color
console = Console()

def display_intro(console_width, current_path):
    """Display the introduction, ASCII art, and current path."""
    os.system("cls" if os.name == "nt" else "clear")
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        fig = Figlet(font = config["banner-font"])
        banner_colour = config["banner-colour"]
    except (pyfiglet.FontNotFound,FileNotFoundError,KeyError) :
        fig = Figlet(font = "bloody")
        banner_colour = "red"

    # Generate ASCII art
    ascii_art_lines = fig.renderText("CODEBASE").split("\n")

    # Print ASCII art at the top, centered
    for line in ascii_art_lines:
        if line.strip():  # Skip empty lines
            console.print(line.center(console_width),style=banner_colour)

    intro_text = (
        "\n[bold cyan]Welcome to the Codebase Project Setup Tool.[/bold cyan]\n"
        "This tool helps you easily manage and organize your programming projects.\n"
        "Type 'exit' or press 'ctrl c' to quit.\n"
    )
    console.print(intro_text, justify="center")

    #Checking if the configs are added
    try:
        with open(CONFIG_FILE,"r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or corrupted file
        data = {}
    
    try:
        if data["is_setup"] == True:
            console.print("[bold]Type 'help' for commands[/bold]", justify="left")            
    except KeyError:
        console.print("[bold]Enter 'setup' to setup your defaults.[/bold]", justify="left")

def main():
    """Main program function."""
    current_width = os.get_terminal_size().columns
    current_path = os.getcwd()

    display_intro(current_width, current_path)



if __name__ == "__main__":
    main()
