import os
import json
from rich.console import Console
from scripts.commands.list import list_templates
from scripts.com_util import project_exists

console = Console()

TEMPLATE_DIR = "templates"

def create_files_from_structure(structure, base_path):

    folder_path = ""
    # Process subfolders and files
    for item in structure.get("folders", []):
        if isinstance(item, dict):  # Ensure item is a dictionary
            create_files_from_structure(item, folder_path)
        else:
            raise ValueError(f"Invalid folder entry: {item}")

    for file in structure.get("files", []):
        file_path = os.path.join(folder_path, file["name"])
        with open(file_path, 'w') as f:
            f.write(file.get("content", ""))
        
            print(f"File created: {file_path}")



def create_project(temp_name, project_name, path: str ="cwd"):

    if ".json" not in temp_name:
         temp_name = temp_name + ".json"

    template_file = os.path.join(TEMPLATE_DIR, f"{temp_name}")
    if not os.path.exists(template_file):
        console.print(f"\n[bold red]Template '[bold yellow]{temp_name}[/bold yellow]' not found.[/bold red]")
        console.print("\nList of availabe templates:")
        list_templates()
        return   
    
    try:
        with open(template_file, 'r') as f :
            data = json.load(f)  
    except json.JSONDecodeError as e:
        console.print(f"\n[bold red]Error[/bold red]{e}")  
        console.print(f"The template seems corrupted...")
        console.print(f"Deleting the template..")
        os.remove(f"{TEMPLATE_DIR}/{temp_name}")
        console.print(f"[yellow]Template deleted successfully.[/yellow]")

    if path == "cwd":
        path = os.getcwd()
    elif "\\" in path:        
        path = path.replace("\\", "/")

    path = os.path.abspath(path.strip())

    #Handle creation of project inside a project (not a valid action)
    project_exists(path)

    #create the root dir------------------------
    folder_path = os.path.join(path, project_name)
    try:
        os.makedirs(folder_path, exist_ok=False)
    except (FileExistsError,FileNotFoundError) as e:
        console.print(f"[bold red]{e}[/bold red]")
        return
    

    


create_project("temp","dj","hey")








