import os
import json

LOG = False

def load_template(template_name):
    """Load a JSON template from the templates directory."""
    template_dir = "templates"
    template_file = os.path.join(template_dir, f"{template_name}.json")
    if not os.path.exists(template_file):
        return -1
    with open(template_file, 'r') as file:
        return json.load(file)

def create_files_from_structure(structure, base_path):
    """Recursively create folders and files from the template structure."""
    # Create the root folder
    folder_path = os.path.join(base_path, structure["name"])
    os.makedirs(folder_path, exist_ok=True)
    if LOG:
        print(f"Folder created: {folder_path}")

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
        if LOG:
            print(f"File created: {file_path}")

def generate_template(template_name):
    """Generate the project structure from the specified template."""
    template_data = load_template(template_name)
    if template_data == -1:
        print(f"Template '{template_name}' not found.")
        return

    # Get current working directory
    current_directory = os.getcwd()
    print(f"Current working directory: {current_directory}")

    # Create structure based on the template
    create_files_from_structure(template_data["structure"], base_path=current_directory)

if __name__ == "__main__":
    LOG = True
    template_name = input("Enter the template name: ").strip()
    generate_template(template_name)
