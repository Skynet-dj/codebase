import os
import json
import subprocess
from rich.console import Console
from scripts.com_util import CONFIG_FILE, COMMANDS_FILE, ar_, tool_name
from scripts.com_util import search_template, search_project
from scripts.commands import create, list_, open_, rm

console = Console()

MissingArgumentError = type(f"MissingArgumentError:", (Exception,), {})

def command_handle(passed_command: str):
    # Load commands and configuration
    try:
        with open(COMMANDS_FILE, "r") as c:
            all_commands = json.load(c)
    except FileNotFoundError:
        console.print(f"[bold red]Error: {COMMANDS_FILE} not found.[/bold red]")
        console.print(f"Try reinstalling the package with 'pip install {tool_name}'")
        return

    # Tokenize the command and flags
    tokenised_command = passed_command.split()
    command = [token for token in tokenised_command if "-" not in token]
    flags = [token for token in tokenised_command if "-" in token]

    # Validate command length
    if len(command) > 3:
        console.print(f"[bold red]Error: more arguments than required[/bold red]")
        return

    # Validate flags
    valid_flags = ["-r", "-p", "-e", "-E", "s"]
    flags = [flag.strip() for flag in flags if flag in valid_flags]

    # Check if both '-e' and '-E' flags are present
    if "-e" in flags and "-E" in flags:
        console.print(f"[bold red][FlagError]: Cannot have both <-e> and <-E> as flags[/bold red]")
        return

    # Check if more than one command is passed (other than 'help')
    if len(command) > 1 and command[0] != "help" and command[0] not in all_commands:
        console.print(f"[bold red][InvalidArgumentError]: Invalid command argument <{command[0]}>[/bold red]")
        return

    # Try to load the config file to get root-path
    try:
        with open(CONFIG_FILE, "r") as f:
            root_path = json.load(f).get("root-path", None)
    except FileNotFoundError:
        root_path = None

    if not command or command[0] not in all_commands:
        subprocess.call(passed_command, shell=True)
        return

    cmd_name = command[0]

    # Command: create
    if cmd_name == "create":
        if len(command) < 2:
            raise MissingArgumentError(cmd_name)

        if command[1] == "project":
            template_name = console.input(f"Template you want to use {ar_}")
            project_name = console.input(f"Project Name {ar_} ")

            # Determine path to create the project
            path = command[2] if len(command) > 2 else None
            if "-r" in flags and root_path:
                path = root_path

            if path:
                create.create_project(template_name, project_name, path)
            else:
                create.create_project(template_name, project_name)

        elif command[1] == "template":
            template_name = console.input(f"Template Name {ar_}")
            from_existing = console.input(f"Create from existing template? (y/n) {ar_} ").strip().lower()
            if from_existing in ("y", "yes"):
                create.create_template(template_name, from_existing=True)
            elif from_existing in ("n", "no"):
                create.create_template(template_name, from_existing=False)
            else:
                console.print(f"[red]Error: Invalid input '{from_existing}'. Expected 'y' or 'n'.[/red]")

    # Command: rm
    elif cmd_name == "rm":
        if len(command) < 3:
            raise MissingArgumentError(cmd_name)

        target = command[1]
        name = command[2]
        if target == "project":
            path = search_project(name, True)
            if not path:
                return
            confirm = "-n" in flags or console.input(f"Sure? (y/n): ").lower() in ("y", "yes")
            if confirm:
                rm.rm_project(path,name)
        elif target == "template":
            path = search_template(name, False, True)
            if not path:
                return
            confirm = "-n" in flags or console.input(f"Sure? (y/n): ").lower() in ("y", "yes")
            if confirm:
                rm.rm_template(path)

    # Command: open
    elif cmd_name == "open":
        if len(command) < 3:
            raise MissingArgumentError(cmd_name)
        target = command[1]
        name = command[2]

        if target == "project":
            path = search_project(name, True)
            if not path:
                return
            if "-e" in flags:                
                open_.open_explorer(path)
            elif "-E" in flags:
                open_.open_explorer(path)
                return
            open_.open_project(path)
            
        elif target == "template":
            path = search_template(name, False, True)
            if path:
                open_.open_template(path)
                return

    # Command: list
    elif cmd_name == "list":
        if len(command) < 2:
            raise MissingArgumentError(cmd_name)

        target = command[1]
        if target == "projects":
            list_.list_projects(flags)
        elif target == "templates":
            list_.list_templates()

    # Command: help
    elif cmd_name == "help":
        if len(command) < 2:
            console.print("[bold blue]Available Commands:[/bold blue]")
            for cmd, details in all_commands.items():
                console.print(f"[bold cyan]{cmd}[/bold cyan]: {details['description']}")
            return
        help_command = command[1]
        if help_command in all_commands:
            details = all_commands[help_command]
            console.print(f"\nCommand [bold blue]{help_command}[/bold blue] Details:")
            console.print(f"[bold cyan]Description[/bold cyan]: {details['description']}")
            console.print(f"[bold cyan]Usage[/bold cyan]: {details['usage']}")
            console.print(f"[bold cyan]Example[/bold cyan]: {details['example']}")
            if "flags" in details:
                console.print(f"[bold cyan]Flags[/bold cyan]: ", end="")
                for i, flag in enumerate(details['flags']):
                    flag_ = flag.split("(")[:-1]
                    flag_desc = "(" + flag.split("(")[-1]
                    console.print(f"{'      '*i}[bold magenta]{' '.join(flag_)}[/bold magenta] {flag_desc}")

    # Command: setup
    elif cmd_name == "setup":
        os.system("python scripts/commands/setup.py")
    elif cmd_name == "exit":
        raise KeyboardInterrupt
    else:
        console.print(f"[bold red]Error: Command '{cmd_name}' not recognized.[/bold red]")