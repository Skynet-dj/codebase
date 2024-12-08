import os
import json
from rich.console import Console
from rich.table import Table
from scripts.com_util import ar_  # Input Arrow

console = Console()

CONFIG_FILE = "data/config.json"
PROJECTS_FILE = "data/projects.json"


def create_config():
    try:
        with open(CONFIG_FILE, "x") as f:
            defaults = {
                "is_setup":False,
                "text-editor": "Micro",
                "text-editor-command": "micro",
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
            return data["is_setup"]


def editor_setup(is_setup):
    if is_setup:
        console.print("\nDefault 'text-editor' is already configured by you.")
        input_ = console.input(f"Do you still want to proceed? (y/n) {ar_} ")
        if input_.lower() in ["n", "no"]:
            return

    editors_available = [
        "Micro",
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
        "micro",
        "vim",
        "nano",
        "emacs",
        "code",
        "pycharm",
        "subl",
        "atom",
    ]

    config = {"text-editor": "", "text-editor-command": ""}

    input_ = console.input(f"\nDo you want to use the default editor 'Micro' (y/n) {ar_} ")
    if input_.lower() in ["y", "yes"]:
        save_to_json({"text-editor": "Micro", "text-editor-command": "micro"})
        console.print(f"\n[bold yellow]Selected Editor: Micro [/bold yellow]")
        return

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
        editor = console.input(f"Editor that you want to use {ar_} ")
        command = console.input(f"CMD command to start the editor {ar_} ")
        config["text-editor"] = editor
        config["text-editor-command"] = command

    save_to_json(config)
    console.print(f"\n[bold yellow]Selected Editor: {config['text-editor']} [/bold yellow]")


def root_path_setup(is_setup):
    if is_setup:
        console.print("\nDefault 'root path' is already configured by you.")
        input_ = console.input(f"Do you still want to proceed? (y/n) {ar_} ")
        if input_.lower() in ["n", "no"]:
            return

    console.print("\nIn the 'root directory' you can store projects using the '-r' flags with 'create command'")
    console.print("By default projects when created will be stored in the 'Current Directory'.")

    while True:
        input_ = console.input(f"Enter absolute path for the 'root' directory {ar_} ").replace("\\", "/")
        if os.path.exists(input_):
            config = {"root-path": input_.replace("/","\\")}
            save_to_json(config)
            console.print(f"\n[bold yellow]Root Directory: {input_} [/bold yellow]")
            break
        else:
            console.print("[bold red]The entered 'path' does not exist. Please try again.[/bold red]")


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
    is_setup = create_config()
    editor_setup(is_setup)
    root_path_setup(is_setup)
    save_to_json({"is_setup": True})

    config_json = "\\".join((os.path.abspath(__file__).split("\\")[:-3] + ["data", "config.json"]))
    console.print(f"To config other variables refer to [magenta]{config_json}[/magenta]")
    console.print(f"[bold yellow]SETUP COMPLETE[/bold yellow]")
except KeyboardInterrupt:
    console.print(f"\n[bold red]Setup Canceled![/bold red]")



