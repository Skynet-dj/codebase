import os
from pyfiglet import Figlet
import pyfiglet
from rich.console import Console
from rich import print
import json
from scripts.com_util import CONFIG_FILE, COMMANDS_FILE,ar_

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
        fig = Figlet(font = "ansi_regular")
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


def help(command: str):
    try:
        # Load the command data from the JSON file
        with open(COMMANDS_FILE, "r") as f:
            commands_data = json.load(f)

        if command in commands_data:
            cmd_info = commands_data[command]

            # Display the command name in bold
            print(f"\n[bold]{command}[/bold]\n")

            # Display description
            if "description" in cmd_info:
                print(f"Description: {cmd_info['description']}\n")

            # Display usage
            if "usage" in cmd_info:
                print(f"Usage: {cmd_info['usage']}\n")

            # Display parameters
            if "parameters" in cmd_info:
                parameters = ', '.join(cmd_info['parameters'])
                print(f"Parameters: {parameters}\n")

            # Display flags with descriptions
            if "flags" in cmd_info:
                print("Flags:")
                for flag in cmd_info["flags"]:
                    print(f"  {flag}")  # Clean flag display

            # Display example
            if "example" in cmd_info:
                print(f"\nExample: {cmd_info['example']}\n")

        else:
            # If the command is not found, provide a suggestion and guidance
            print(f"Command '{command}' not found!")
            print("Try `pycmd help` for a list of all available commands.")
            similar_commands = [cmd for cmd in commands_data if cmd.startswith(command[0])]  # Suggest commands starting with the same letter
            if similar_commands:
                print("\nDid you mean one of these?")
                for cmd in similar_commands:
                    print(f"  {cmd}")
            else:
                print("No similar commands found.")

    except FileNotFoundError:
        print("Commands file not found! Make sure the path to the JSON file is correct.")
    except json.JSONDecodeError:
        print("There was an issue reading the commands file. It may be corrupted.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        

#-------here comes the "main" part of the code----------------#

#COLOR MAPPING (with rich):
#1.Prompt text                = Null
#2.Warning text               = Bold Red
#3.Task completion text       = Bold Yellow
#4.Command name               = Bold Green
#5.Command Usage              = Bold Blue
#6.Input Arrow: ">>"          = Bold Red
#7.Path                       = Magenta
#I'm gonna use any color I like for the tables 

current_width = os.get_terminal_size().columns
current_path = os.getcwd()

display_intro(current_width, current_path)

