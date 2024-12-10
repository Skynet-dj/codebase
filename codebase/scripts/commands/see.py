import subprocess
from rich.console import Console
from rich.tree import Tree
from codebase.scripts.com_util import search_template, search_project

console = Console()

def see_template(name):
    data =  search_template(name)
    if not data:
        return    
    def create_tree(node, parent_tree):
        # Add folders first
        if 'folders' in node:
            for folder in node['folders']:
                folder_tree = parent_tree.add(folder['name'])
                create_tree(folder, folder_tree)
        # Add files under the current folder
        if 'files' in node:
            for file in node['files']:
                parent_tree.add(f"{file['name']}")
    root = Tree(f"Project: {data['metadata']['name_of_template']}")
    create_tree(data['structure'], root)
    console.print(root)

def see_project(name):
    path = search_project(name, True)
    if not path:
        return
    subprocess.run(f"tree {path}", shell=True)