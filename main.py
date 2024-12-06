import os
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from pyfiglet import Figlet
import time

console = Console()

def display_intro(console_width):
    os.system("cls" if os.name == "nt" else "clear")
    fig = Figlet(font="standard")
    ascii_art_lines = fig.renderText("Codebase").split("\n")
    for line in ascii_art_lines:
        if line.strip():
            console.print(line.center(console_width), style="bold yellow")
    intro_text = (
        "\nWelcome to the Codebase Project Setup Tool.\n"
        "This tool helps you easily manage and organize your programming projects.\n"
        "Use it to create, configure, and maintain your project files efficiently.\n"
        "Resize the terminal to see it adjust dynamically. Press Ctrl+C to quit.\n"
    )
    console.print(intro_text, style="bold cyan", justify="center")

def create_project_structure(project_name):
    base_dirs = ["src", "tests", "docs", "configs"]
    try:
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=True)
        for directory in base_dirs:
            (project_path / directory).mkdir(exist_ok=True)
        (project_path / "README.md").write_text(f"# {project_name}\n\nProject Description.\n")
        console.print(f"[bold green]Project {project_name} created successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error creating project: {e}[/bold red]")

def show_help():
    help_text = """
Available Commands:
  1. create_project - Set up a new project structure.
  2. manage_deps    - Install or manage project dependencies.
  3. exit           - Exit the tool.
    """
    console.print(help_text, style="bold cyan")

def main():
    display_intro(os.get_terminal_size().columns)
    console.print("[bold yellow]Welcome to the Codebase Setup Tool![/bold yellow]")
    while True:
        command = Prompt.ask("[bold cyan]Enter a command (type 'help' for options)[/bold cyan]").strip()
        if command == "create_project":
            project_name = Prompt.ask("[bold green]Enter the project name[/bold green]")
            create_project_structure(project_name)
        elif command == "help":
            show_help()
        elif command == "exit":
            console.print("[bold red]Exiting the tool. Goodbye![/bold red]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid command! Type 'help' to see available commands.[/bold red]")
main()
