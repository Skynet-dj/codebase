import os
import json
from rich.console import Console
from rich.table import Table
from codebase.scripts.com_util import CONFIG_FILE, PROJECTS_FILE, ar_,text_editor

console = Console()

def create_config(root_path = False):
    try:
        with open(CONFIG_FILE, "x") as f:
            defaults = {
                "is_setup":False,
                "text-editor": "Notepad",
                "text-editor-command": "notepad",
                "root-path": "",
                "banner-font": "ansi_regular",
                "banner-color": "red",
            }
            json.dump(defaults, f, indent=4)
        with open(PROJECTS_FILE, "x") as f:
            json.dump({}, f, indent=4)
        return False
    except FileExistsError:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            if root_path:
                return data["root-path"]
            return data["is_setup"]


def editor_setup(is_setup):
    if is_setup:
        console.print("\nDefault 'text-editor' is already configured by you.")
        input_ = console.input(f"Do you still want to proceed? (y/n) {ar_} ")
        if input_.lower() in ["n", "no"]:
            return

    editors_available = [
        "Pyvim",
        "Notepad",
        "Vim",
        "GNU Nano",
        "GNU Emacs",
        "Visual Studio Code",
        "PyCharm",
        "Sublime Text",
        "Atom",
        "Other",
    ]

    editor_commands = [
        "pyvim"
        "notepad",
        "vim",
        "nano",
        "emacs",
        "code",
        "pycharm",
        "subl",
        "atom",
    ]

    config = {"text-editor": "", "text-editor-command": ""}

    input_ = console.input(f"\nDo you want to use the default editor '{text_editor}' (y/n) {ar_} ")
    if input_.lower() in ["y", "yes"]:
        console.print(f"[bold yellow]Selected Editor: Micro [/bold yellow]")
        return  {"text-editor": "Micro", "text-editor-command": "micro"}

    table = Table(show_header=True, style="bold cyan")
    table.add_column("Editors", style="bold red")
    for i, editor in enumerate(editors_available, start=1):
        table.add_row(f"{i}. {editor}", style="bold green")
    console.print(table)

    console.print("\nYou should have the editor already installed or install it after the setup.")

    while True:
        try:
            editor_index = int(console.input(f"Enter the Index number {ar_} ").strip())
            if 1 <= editor_index <= len(editors_available):
                break
            else:
                console.print("[bold red]Invalid index. Please select a valid option.[/bold red]")
        except ValueError:
            console.print("[bold red]Please enter a valid integer for the index.[/bold red]")

    config["text-editor"] = editors_available[editor_index - 1]

    if editor_index <= len(editor_commands):
        config["text-editor-command"] = editor_commands[editor_index - 1]
    else:  # For "Other"
        editor = console.input(f"\nEditor that you want to use {ar_} ")
        command = console.input(f"CMD command to start the editor {ar_} ")
        config["text-editor"] = editor
        config["text-editor-command"] = command

    
    console.print(f"[bold yellow]Selected Editor: {config['text-editor']} [/bold yellow]")
    return config


def root_path_setup(root_path):
    if root_path:
        console.print(f"\nDefault 'root path' is already configured by you, Root-Path --> {root_path}")
        input_ = console.input(f"Do you still want to proceed? (y/n) {ar_} ")
        if input_.lower() in ["n", "no"]:
            return

    console.print("\nIn the 'root directory' you can store projects using the '-r' flags with 'create command'")
    console.print("By default projects when created will be stored in the 'Current Directory'.")

    while True:
        input_ = console.input(f"Enter absolute path for the 'root' directory (blank to skip){ar_} ").replace("\\", "/")
        if os.path.exists(input_):
            config = {"root-path": input_.replace("/","\\")}
            console.print(f"\n[bold yellow]Root Directory: {input_} [/bold yellow]")
            return config
        elif not input_:
            return
        else:
            console.print("\n[bold red]The entered 'path' does not exist. Please try again.[/bold red]")


def save_to_json(config):
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or corrupted file
        data = {}
    data.update(config)

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)



try:
    console.print(f"\n[bold cyan]Welcome to SETUP[/bold cyan]")
    is_setup = create_config()
    config1 = editor_setup(is_setup)
    root_path = create_config(True)
    config2 = root_path_setup(root_path)

    save_to_json(config1)
    if config2:
        save_to_json(config2)
    save_to_json({"is_setup": True})

    config_json = "\\".join((os.path.abspath(__file__).split("\\")[:-3] + ["data", "config.json"]))
    console.print(f"\nTo config other variables refer to [magenta]{config_json}[/magenta]")
    console.print(f"[bold yellow]SETUP COMPLETE[/bold yellow]")
except KeyboardInterrupt:
    console.print(f"\n\n[bold red]Setup Canceled! The changes won't be added![/bold red]")



