import os
import json
from rich.console import Console
from scripts.commands.list_ import list_templates
from scripts.com_util import project_exists, update_project, TEMPLATE_DIR, ar_, search_template
from scripts.commands.open_ import open_template
import shutil

console = Console()
    
def create_project(temp_name, project_name, path = os.getcwd()) -> bool:
    temp_data = search_template(temp_name)
    if not temp_data:
        return 

    if "\\" in path:        
        path = path.replace("\\", "/")

    path = os.path.abspath(path.strip())

    #path to be used from now on------------------------#
    folder_path = os.path.join(path, project_name)

    #Handle creation of project inside a project (not a valid action)
    if project_exists(folder_path):
        console.print(f"Project already exists.")
        return

    #create the root dir------------------------    
    try:
        os.makedirs(folder_path, exist_ok=False)
    except (FileExistsError,FileNotFoundError) as e:
        console.print(f"[bold red]{e}[/bold red]")
        return
    
      # Function to create project structure based on the JSON template
    def create_files_from_structure(structure, base_path):
        try:
            # Create subfolders
            for folder in structure.get("folders", []):
                if isinstance(folder, dict):  # Ensure each folder is a dictionary
                    folder_path = os.path.join(base_path, folder["name"])
                    os.makedirs(folder_path, exist_ok=True)
                    create_files_from_structure(folder, folder_path)

            # Create files
            for file in structure.get("files", []):
                file_path = os.path.join(base_path, file["name"])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure parent directories exist
                with open(file_path, 'w') as f:
                    f.write(file.get("content", ""))  # Write file content

        except ValueError as e:
            console.print(f"[bold red]{e}[/bold red]")
            console.print(f"Would you like to edit the template (else delete it)? (y/n)")
            input_ = console.input(f"{ar_}")
            if input_.lower() == ("y" or "yes"):
                console.print(f"Try editing it with 'open template {temp_name}'")
                return
            console.print(f"Deleting the template...")
            os.remove(f"{TEMPLATE_DIR}/{temp_name}")
            os.remove(f"{folder_path}")
            console.print(f"[yellow]Template deleted successfully.[/yellow]")
            return

    folder_path = os.path.join(path, project_name.replace(" ", "_"))
    os.makedirs(folder_path, exist_ok=True)

    create_files_from_structure(temp_data["structure"], folder_path)

    update_project(folder_path, project_name)
    console.print(f"[bold yellow]Project created successfully.[/bold yellow]")
    return True


def create_template(temp_name: str, from_existing: bool=False) -> None :    
    if from_existing:
        console.print(f"Enter template to use ")
        temp = console.input(f"{ar_} ")
        if search_template(temp, want_data=False):
            shutil.copy(f'{TEMPLATE_DIR}/{temp}.json', f'{TEMPLATE_DIR}/{temp_name}.json')
            #open the template in the configured editor 
            open_template(temp_name)
            return
    try:
        with open(f"{TEMPLATE_DIR}/{temp_name}.json", "x") as f:
            json.dump({},f)
    except FileExistsError as e:
        console.print(f"[bold red]{e}[/bold red]")
        console.print(f"Use 'list template' to see existing templates")
        return 
    return True
