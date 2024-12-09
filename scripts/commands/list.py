import os
from scripts.com_util import Table, console, projects, TEMPLATE_DIR

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


def list_templates():
    table = Table(show_header=True, header_style="cyan")
    table.add_column("Template_Name", style="yellow")
    
    if not os.path.exists(TEMPLATE_DIR):
        console.print(f"[bold red]Template directory '{TEMPLATE_DIR}' does not exist![/bold red]")
        console.print(f"Try reinstalling the package")
        return
    
    # Get the list of template files
    try:
        template_files = [f for f in os.listdir(TEMPLATE_DIR) if os.path.isfile(os.path.join(TEMPLATE_DIR, f))]
    except Exception as e:
        console.print(f"[bold red]Error accessing template directory:[/bold red] {e}")
        return

    if template_files:
        for template_file in template_files:
            table.add_row(template_file.split(".")[0])
        console.print(table)
    else:
        console.print("[bold green]No templates available in the directory.[/bold green]")


