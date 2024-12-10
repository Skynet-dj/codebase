import os
import json
import subprocess
from pyfiglet import Figlet
import pyfiglet
from rich.console import Console
from codebase.scripts.com_util import CONFIG_FILE, ar_, tool_name
from codebase.scripts.com_util import banner_color, banner_font
from codebase.scripts.command_handle import command_handle, MissingArgumentError
  

# Initialize the console from Rich for color
console = Console()    

def display_intro(console_width, current_path):
    """Display the introduction, ASCII art, and current path."""

    subprocess.call("cls" if os.name == "nt" else "clear", shell=True)    
    while True:
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            fig = Figlet(font =config["banner-font"])
            banner_colour = config["banner-color"]   
            break
        except (FileNotFoundError,KeyError):
            fig = Figlet(font = banner_font)
            banner_colour = banner_color
            break
        except pyfiglet.FontNotFound:
            subprocess.call(f"python codebase/scripts/install_fonts.py", shell=True)

    # Generate ASCII art
    ascii_art_lines = fig.renderText(f"{tool_name.upper()}").split("\n")

    # Print ASCII art at the top, centered
    for line in ascii_art_lines:
        if line.strip():  # Skip empty lines
            console.print(line.center(console_width),style=banner_colour)

    intro_text = (
        f"\n[bold cyan]Welcome to the {tool_name} Project Setup Tool.[/bold cyan]\n"
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
    
    do_setup = False
    try:
        if data["is_setup"] == True:
            console.print("[bold]Type 'help' for commands[/bold]", justify="left")
        else:
            do_setup = True
    except KeyError:
        do_setup = True
    if do_setup:
        console.print("[bold]Enter 'setup' to setup your defaults.[/bold]", justify="left")



#-------here comes the "main" part of the code----------------#

#COLOR MAPPING (with rich):
#0.Welcome text               = Bold Cyan
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

#---the even loop------#
try:
    while True:
        input_ = console.input(f"{ar_} ")
        if not input_:
            continue
        try:
            command_handle(input_)
        except (MissingArgumentError) as e:
            console.print(f"[bold red]MissingArgumentError: Missing argument for '{e}'[/bold red]")
            command_handle(f"help {e}")
            print()
        except(subprocess.CalledProcessError) as e:
            console.print(f"[bold red]{e}[/bold red]")
except KeyboardInterrupt:
    console.print(f"[bold yellow]Exiting the program...[/bold yellow]")