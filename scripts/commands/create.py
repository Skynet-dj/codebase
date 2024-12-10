import os
import json
from rich.console import Console
from scripts.commands.list_ import list_templates
from scripts.com_util import project_exists, update_project, TEMPLATE_DIR, ar_, search_template
from scripts.commands.open_ import open_template
import shutil

console = Console()
    
def create_project(temp_name, project_name, path: str = "cwd") -> bool:
    # Load template data (updated with static values)
    temp_data = search_template(temp_name)
    if not temp_data:
        console.print(f"[bold red]Template '{temp_name}' not found.[/bold red]")
        return False

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

        except Exception as e:
            console.print(f"[bold red]Error creating structure: {e}[/bold red]")
            return False

    # Set the project folder path
    folder_path = os.path.join(os.path.abspath(path), project_name.replace(" ", "_"))

    try:
        os.makedirs(folder_path, exist_ok=False)  # Ensure the project folder is created
        create_files_from_structure(temp_data["structure"], folder_path)  # Create the project structure
        update_project(folder_path, project_name)  # Update project record
        console.print(f"[bold yellow]Project '{project_name}' created successfully.[/bold yellow]")
        return True
    except FileExistsError:
        console.print(f"[bold red]Project '{project_name}' already exists.[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        return False


def create_template(temp_name: str, from_existing: bool=False) -> None :    
    if from_existing:
        temp = console.input(f"Enter template to use {ar_} ")
        if search_template(temp, want_data=False):
            shutil.copy(f'{TEMPLATE_DIR}/{temp}.json', f'{TEMPLATE_DIR}/{temp_name}.json')
            #open the template in the configured editor 
            open_template(temp_name)
            return
    try:
        with open(f"{TEMPLATE_DIR}/{temp_name}.json", "x") as f:
            json.dump({},f)
            
        return "op"
    except FileExistsError as e:
        console.print(f"[bold red]{e}[/bold red]")
        console.print(f"Use 'list template' to see existing templates")
        return
    return True

