import os
import json
from scripts.commands import create, list_, open_
while True:
    try:
        from pyfiglet import Figlet
        import pyfiglet
        from rich.console import Console
        from rich import print
        from scripts.com_util import CONFIG_FILE, COMMANDS_FILE,ar_
        break
    except (ModuleNotFoundError,ImportError,):
        print("Few requirements are not satisfied.")
        os.system("pip install r scripts/requirements.txt")

# Initialize the console from Rich for color
console = Console()    

def display_intro(console_width, current_path):
    """Display the introduction, ASCII art, and current path."""

    os.system("cls" if os.name == "nt" else "clear")    
    while True:
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            fig = Figlet(font = config["banner-font"])
            banner_colour = config["banner-color"]   
            break
        except (FileNotFoundError,KeyError):
            fig = Figlet(font = "ansi_regular")
            banner_colour = "red"
            break
        except pyfiglet.FontNotFound:
            os.system(f"python scripts/install_fonts.py")

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
        


def command_handle(passed_command: str):
    tokenised_command = passed_command.split()
    command = [token for token in tokenised_command if "-" not in token]
    flags = [token for token in tokenised_command if "-" in token]

    # Load commands and configuration
    try:
        with open(COMMANDS_FILE, "r") as c:
            all_commands = json.load(c)
    except FileNotFoundError:
        console.print(f"[red]Error: {COMMANDS_FILE} not found.[/red]")
        return

    try:
        with open(CONFIG_FILE, "r") as f:
            root_path = json.load(f).get("root-path", None)
    except FileNotFoundError:
        root_path = None

    if not command or command[0] not in all_commands:
        os.system(passed_command)
        return

    cmd_name = command[0]

    # Command: create
    if cmd_name == "create":
        if len(command) < 2:
            console.print("[red]Error: Missing arguments for 'create'.[/red]")
            return

        if command[1] == "project":
            template_name = console.input("Template you want to use: ")
            project_name = console.input("Project Name: ")

            # Determine path to create the project
            path = command[2] if len(command) > 2 else None
            if "-r" in flags and root_path:
                path = root_path

            if path:
                create.create_project(template_name, project_name, path)
            else:
                create.create_project(template_name, project_name)

        elif command[1] == "template":
            template_name = console.input("Template Name: ")
            from_existing = console.input("Create from existing template? (y/n): ").strip().lower()
            if from_existing in ("y", "yes"):
                create.create_template(template_name, from_existing=True)
            elif from_existing in ("n", "no"):
                create.create_template(template_name, from_existing=False)
            else:
                console.print(f"[red]Error: Invalid input '{from_existing}'. Expected 'y' or 'n'.[/red]")

    # Command: rm
    elif cmd_name == "rm":
        if len(command) < 2:
            console.print("[red]Error: Missing arguments for 'rm'.[/red]")
            return
        target = command[1]
        if target == "project":
            project_name = command[2] if len(command) > 2 else console.input("Project Name: ")
            confirm = "-n" in flags or console.input(f"Confirm removal of project '{project_name}'? (y/n): ").lower() in ("y", "yes")
            if confirm:
                console.print(f"[bold red]Project '{project_name}' removed (placeholder logic).[/bold red]")
        elif target == "template":
            template_name = command[2] if len(command) > 2 else console.input("Template Name: ")
            confirm = "-n" in flags or console.input(f"Confirm removal of template '{template_name}'? (y/n): ").lower() in ("y", "yes")
            if confirm:
                console.print(f"[bold red]Template '{template_name}' removed (placeholder logic).[/bold red]")

    # Command: open
    elif cmd_name == "open":
        if len(command) < 3:
            console.print("[red]Error: Missing arguments for 'open'.[/red]")
            return
        target = command[1]
        name = command[2]
        if target == "project":
            if "-e" in flags or "-E" in flags:
                path = f"Path for project '{name}' (placeholder logic)"
                open_.open_explorer(path)
            else:
                open_.open_project(name)
        elif target == "template":
            if "-e" in flags or "-E" in flags:
                path = f"Path for template '{name}' (placeholder logic)"
                open_.open_explorer(path)
            else:
                open_.open_template(name)

    # Command: list
    elif cmd_name == "list":
        if len(command) < 2:
            console.print("[bold red]Error: Missing arguments for 'list'.[/bold red]")
            return
        target = command[1]
        if target == "projects":
            list_.list_projects(flags)
        elif target == "templates":
            list_.list_templates()

    # Command: help
    elif cmd_name == "help":
        if len(command) < 2:
            console.print("[blue]Available Commands:[/blue]")
            for cmd, details in all_commands.items():
                console.print(f"[bold cyan]{cmd}[/bold cyan]: {details['description']}")
            return
        help_command = command[1]
        if help_command in all_commands:
            details = all_commands[help_command]
            console.print(f"[blue]{help_command} Command Details:[/blue]")
            console.print(f"  [cyan]Description[/cyan]: {details['description']}")
            console.print(f"  [cyan]Usage[/cyan]: {details['usage']}")
            console.print(f"  [cyan]Example[/cyan]: {details['example']}")
            if "flags" in details:
                console.print(f"  [cyan]Flags[/cyan]: {', '.join(details['flags'])}")

    # Command: setup
    elif cmd_name == "setup":
        os.system("python scripts/commands/setup.py")

    else:
        console.print(f"[bod red]Error: Command '{cmd_name}' not recognized.[/bold red]")
    

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

        InvalidInputError = type("InvalidInputError", (Exception,), {})
        try:
            command_handle(input_)
        except InvalidInputError as e:
            console.print(f"[bold red]{e}[/bold red]")
        print()

except KeyboardInterrupt:
    console.print(f"[bold yellow]Exiting the program...[/bold yellow]")
