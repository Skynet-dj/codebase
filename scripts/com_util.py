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
