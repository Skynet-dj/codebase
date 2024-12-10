import os
import json
from rich.console import Console
from scripts.commands.list_ import list_templates
from scripts.com_util import project_exists, update_project, TEMPLATE_DIR, ar_, search_template
from scripts.commands.open_ import open_template
import shutil

console = Console()
    
def create_project(temp_name, project_name, path: str = "cwd") -> bool:
    temp_data = search_template(temp_name)
    if not temp_name:
        return 
    
    
    # Collect required variables for placeholders in the template
    variables = {}
    placeholders = set()

    # Recursively check folders and files for placeholders
    def find_placeholders(structure):
        if isinstance(structure, dict):
            for key, value in structure.items():
                if isinstance(value, str):
                    # Check for placeholders in strings ({{}})
                    if '{{' in value and '}}' in value:
                        placeholders.add(value.strip("{}").strip())
                # Recursively check folders and files
                elif isinstance(value, (dict, list)):
                    find_placeholders(value)
        elif isinstance(structure, list):
            for item in structure:
                find_placeholders(item)

    # Find placeholders in the template structure
    find_placeholders(temp_data)

    # Prompt for each placeholder if not already in variables
    for placeholder in placeholders:
        if placeholder not in variables:
            value = console.input(f"[bold green]Enter value for {placeholder.replace('_', ' ')}: [/bold green]").strip()
            variables[placeholder] = value if value else f"{{{{ {placeholder} }}}}"

    # Recursive function to replace placeholders in content
    def replace_placeholders(content, variables):
        for placeholder, value in variables.items():
            content = content.replace(f"{{{{ {placeholder} }}}}", value)
        return content

    # Function to create project structure
    def create_files_from_structure(structure, base_path):
        try:
            # Replace variables in the current structure
            if isinstance(structure, dict):
                structure = {key: replace_placeholders(value, variables) if isinstance(value, str) else value
                             for key, value in structure.items()}

            # Create subfolders
            for item in structure.get("folders", []):
                if isinstance(item, dict):  # Ensure item is a dictionary
                    folder_path = os.path.join(base_path, item["name"])
                    os.makedirs(folder_path, exist_ok=True)
                    create_files_from_structure(item, folder_path)

            # Create files
            for file in structure.get("files", []):
                file_path = os.path.join(base_path, file["name"])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure parent directories exist
                with open(file_path, 'w') as f:
                    content = file.get("content", "")
                    f.write(replace_placeholders(content, variables))  # Replace content variables

        except ValueError as e:
            console.print(f"[bold red]{e}[/bold red]")
            console.print(f"Would you like to edit the template (else delete it)? (y/n)")
            input_ = console.input(f"{ar_}")
            if input_.lower() == ("y" or "yes"):
                console.print("Try creating the project again.")
                return
            console.print(f"Deleting the template...")
            os.remove(f"{TEMPLATE_DIR}/{temp_name}")
            os.remove(f"{folder_path}")
            console.print(f"[yellow]Template deleted successfully.[/yellow]")
            return

    folder_path = os.path.join(path, project_name.replace(" ", "_"))
    os.makedirs(folder_path, exist_ok=False)

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
            
        return "op"
    except FileExistsError as e:
        console.print(f"[bold red]{e}[/bold red]")
        console.print(f"Use 'list template' to see existing templates")
        return
    return True

