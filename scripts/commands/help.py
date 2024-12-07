import json
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Initialize the console for printing styled text
console = Console()

# Path to the commands.json file in the 'data' directory
COMMANDS_FILE = "data/commands.json"

# Function to load the commands data from the JSON file
def load_commands():
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, 'r') as f:
            return json.load(f)
    else:
        console.print("[bold red]Error:[/bold red] commands.json file not found.")
        return {}

# Function to display the help information for a specific command
def show_command_help(command_name):
    commands = load_commands()
    
    if command_name not in commands:
        console.print(f"[bold red]Error:[/bold red] No such command '{command_name}'")
        return

    command = commands[command_name]
    
    table = Table(title=f"[bold green]{command_name.upper()} Command Help[/bold green]", show_header=False, box="ROUND")
    table.add_row(f"[bold cyan]Description:[/bold cyan] {command.get('description', 'No description available.')}")
    table.add_row(f"[bold cyan]Usage:[/bold cyan] {command.get('usage', 'No usage information available.')}")
    table.add_row(f"[bold cyan]Example:[/bold cyan] {command.get('example', 'No example available.')}")
    
    if 'flags' in command:
        table.add_row(f"[bold cyan]Flags:[/bold cyan]")
        for flag in command['flags']:
            table.add_row(f"    {flag}")
    
    console.print(table)

# Function to display the general help
def show_general_help():
    commands = load_commands()

    table = Table(title="Available Commands", show_header=True, box="ROUND")
    table.add_column("Command", style="bold green", no_wrap=True)
    table.add_column("Description", style="bold cyan", no_wrap=True)

    for command_name, command_info in commands.items():
        table.add_row(command_name, command_info.get("description", "No description"))

    console.print(table)

def main():
    # Display the general help if no command is provided
    console.print("[bold yellow]Welcome to the Command Help System![/bold yellow]")
    console.print("For general help, type [bold cyan]help[/bold cyan]. For a specific command, use [bold cyan]help <command_name>[/bold cyan].\n")
    
    while True:
        user_input = console.input("[bold cyan]Enter command for help (or 'exit' to quit): [/bold cyan]").strip()

        if user_input.lower() == "exit":
            console.print("[bold yellow]Exiting Help System...[/bold yellow]")
            break
        elif user_input.lower() == "help":
            show_general_help()
        else:
            show_command_help(user_input)

if __name__ == "__main__":
    main()
