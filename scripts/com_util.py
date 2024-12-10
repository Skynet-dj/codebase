import json
import os
from rich.console import Console
from rich.table import Table

console = Console()

#common var/constants to be used throught the package
ar_ = "[bold red]>>[/bold red]"
CONFIG_FILE = "data/config.json"
PROJECTS_FILE = "data/projects.json"
TEMPLATE_DIR = "templates"
COMMANDS_FILE = "data/commands.json"
FONT_DIR = "fonts"


try:
    with open(PROJECTS_FILE, "r") as p:
        projects = json.load(p)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    with open(PROJECTS_FILE, "w") as p:
        json.dump({}, p, indent=4)
    projects = {}


def search_template(temp_name: str, want_data: bool=True):
    if ".json" not in temp_name:
        temp_name = temp_name + ".json"

    template_file = os.path.join(TEMPLATE_DIR, f"{temp_name}")
    if not os.path.exists(template_file):
        console.print(f"\n[bold red]Template '[bold yellow]{temp_name}[/bold yellow]' not found.[/bold red]")
        console.print("Use 'list template' to see existing templates")
        return

    # Loading template data
    try:
        with open(template_file, 'r') as f:
            if want_data:
                return json.load(f)
            return True
    except json.JSONDecodeError as e:
        console.print(f"\n[bold red]Error: [/bold red]{e}")
        console.print(f"The template seems corrupted...")
        console.print(f"Deleting the template...")
        os.remove(f"{TEMPLATE_DIR}/{temp_name}")
        console.print(f"[yellow]Template deleted successfully.[/yellow]")
        return
    
def project_exists(path: str, projects=projects) -> bool:
    if not projects:
        return False
    def search_in_structure(structure):
        for project_name, project_paths_list in structure.items():
            if not project_paths_list:
                continue
            for project_path in project_paths_list:
                if os.path.commonpath([path, project_path]) == project_path:
                    return True
        return False
    return search_in_structure(projects)


def update_project(path: str, project_name: str, project_should_exist = False):    
    if project_name not in projects.keys() :
        projects[project_name] = []

    if project_should_exist:
        projects[project_name].remove(path)
    else:
        projects[project_name].append(path)

    # Safely write the updated data to the JSON file    
    try:
        temp_file = PROJECTS_FILE + ".tmp"
        with open(temp_file, "w") as p:
            json.dump(projects, p, indent=4)
        os.replace(temp_file, PROJECTS_FILE)  # Replace the original file atomically
    except Exception as e:
        print(f"Failed to write data: {e}")
