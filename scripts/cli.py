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
    ascii_art_lines = fig.renderText("Codebase").split("\n")

    # Print ASCII art at the top, centered
    for line in ascii_art_lines:
        if line.strip():  # Skip empty lines
            console.print(line.center(console_width), style="bold yellow")

    intro_text = (
        "\n[bold cyan]Welcome to the Codebase Project Setup Tool.[/bold cyan]\n"
        "[cyan]This tool helps you easily manage and organize your programming projects.[/cyan]\n"
        "[cyan]Resize the terminal to see it adjust dynamically. Type 'exit' to quit.[/cyan]\n"
    )
    console.print(intro_text, justify="center")

    # Print the current working directory
    console.print(f"[bold green]{current_path}[/bold green] >>", end=" ")

def handle_command(command):
    """Handle user commands."""
    if command == "exit":
        return "exit"
    elif command == "help":
        return "[bold green]Available commands:[/bold green]\n- help\n- clear\n- exit"
    elif command == "clear":
        os.system("cls" if os.name == "nt" else "clear")
        return "[bold magenta]Screen cleared![/bold magenta]"
    else:
        return f"[bold red]Unknown command:[/bold red] {command}. Type '[bold green]help[/bold green]' for a list of commands."

def main():
    """Main program function."""
    current_width = os.get_terminal_size().columns
    current_path = os.getcwd()

    display_intro(current_width, current_path)

    try:
        while True:
            # Check if the terminal size has changed
            new_width = os.get_terminal_size().columns
            if new_width != current_width:
                current_width = new_width
                display_intro(current_width, current_path)

            # Check if the current working directory has changed
            new_path = os.getcwd()
            if new_path != current_path:
                current_path = new_path
                console.print(f"\n[bold green]Path changed to:[/bold green] {current_path}")

            # Take command input after the prompt
            command = console.input().strip()

            # Handle the command
            response = handle_command(command)
            if response == "exit":
                console.print("\n[bold red]Exiting... Goodbye![/bold red]")
                break
            console.print(response)

            # Sleep briefly to reduce CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting... Goodbye![/bold red]")




if __name__ == "__main__":
    main()
