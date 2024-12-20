import os
import json
import subprocess
from rich.console import Console
from codebase.scripts.com_util import CONFIG_FILE, COMMANDS_FILE, ar_, tool_name
from codebase.scripts.com_util import search_template, search_project, root_path
from codebase.scripts.commands import create, list_, open_, rm, see

console = Console()

MissingArgumentError = type(f"MissingArgumentError:", (Exception,), {})

def command_handle(passed_command: str):
    # Load commands and configuration
    def load_command():
        try:
            with open(COMMANDS_FILE, "r") as c:
                return json.load(c)
        except FileNotFoundError:
            console.print(f"[bold red]Error: {COMMANDS_FILE} not found.[/bold red]")
            console.print(f"Try reinstalling the package with 'pip install {tool_name}'")
            return
    all_commands = load_command()
    
    # Tokenize the command and flags
    tokenised_command = passed_command.split()
    command = [token for token in tokenised_command if "-" not in token]
    flags = [token for token in tokenised_command if "-" in token]

    # Validate the command list
    if not command:
        console.print("[bold red]Error: No command provided![/bold red]")
        return
    

    # Validate against known commands
    if command[0] not in all_commands :
        subprocess.run(passed_command, shell=True)
        return

    # Process recognized commands
    cmd_name = command[0]

    # Command: create
    if cmd_name == "create":
        if len(command) < 2:
            raise MissingArgumentError(cmd_name)

        if command[1] == "project":
            template_name = console.input(f"Template you want to use {ar_} ")
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
        if command[1] == "config":
            open_.open_project(f"{CONFIG_FILE}")
            return
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

    #command: see
    elif cmd_name == "see":
        if len(command) <3:
            raise MissingArgumentError(cmd_name)
        target = command[1]
        name = command[2]

        if target == "project":
            see.see_project(name)
        elif target == "template":
            see.see_template(name)

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
            console.print(f"Command [bold blue]{help_command}[/bold blue] Details:")
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
        os.system("python codebase/scripts/commands/setup.py")
    elif cmd_name == "exit":
        raise KeyboardInterrupt
    else:
        console.print(f"[bold red]Error: Command '{cmd_name}' not recognized.[/bold red]")