import json
import os
from rich.console import Console
from rich.table import Table

console = Console()

ar_ = "[bold red]>>[/bold red]"
PROJECTS_FILE = "data/projects.json"

try:
    with open(PROJECTS_FILE, "r") as p:
        projects = json.load(p)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    with open(PROJECTS_FILE, "w") as p:
        json.dump({}, p, indent=4)
    projects = {}




def project_exists(path: str, projects=projects) -> bool:
    def search_in_structure(structure):
        for key, substructure in structure.items():
            for project_id, project in substructure.items():
                project_path = os.path.abspath(project["path"])
                if os.path.commonpath([path, project_path]) == project_path:
                    return True
        return False
    return search_in_structure(projects)


def update_project(path: str, project_name: str, projects=projects):
    project_path = os.path.abspath(path)
    
    if project_name not in projects:
        projects[project_name] = {}

    project_id = len(projects[project_name]) + 1
    projects[project_name][str(project_id)] = {"path": project_path}


    # Safely write the updated data to the JSON file    
    try:
        temp_file = PROJECTS_FILE + ".tmp"
        with open(temp_file, "w") as p:
            json.dump(projects, p, indent=4)
        os.replace(temp_file, PROJECTS_FILE)  # Replace the original file atomically
    except Exception as e:
        print(f"Failed to write data: {e}")

def list_projects(flags=None):
    table = Table(show_header=True, header_style="magenta", title="PROJECTS")
    table.add_column("Project_Name")

    all_names = []
    all_paths = []
    filtered_names = []
    filtered_paths = []


    if flags:
        if '-p' in flags:
            table.add_column("Path", style="green")
            for project_name, project_paths_list in projects.items():
                for project_path in project_paths_list:
                    all_names.append(project_name)
                    all_paths.append(project_path)

        if '-s' in flags:
            path = os.getcwd()
            for project_name, project_paths_list in projects.items():
                for project_path in project_paths_list:
                    if os.path.commonpath([path, project_path]) == path:
                        filtered_names.append(project_name)
                        filtered_paths.append(project_path)
            all_names = list(set(all_names).intersection(filtered_names))
            all_paths = [all_paths[all_names.index(name)] for name in all_names]
    else:
        for project_name in projects.keys():
            all_names.append(project_name)
            all_paths.append("-")

    for name, pth in zip(all_names, all_paths):
        if pth == "-":
            table.add_row(name)
        else:
            table.add_row(name,pth)

    if table.row_count > 0:
        console.print(table)
        return
    console.print("[bold green]No projects present[/bold green]")
  

list_projects("-p")