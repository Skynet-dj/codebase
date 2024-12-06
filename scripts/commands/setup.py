import os
import json
from rich.console import Console

CONFIG_FILE = "data/config.json"

# Create the default config file if it doesn't exist
try:
    with open(CONFIG_FILE, "x") as f:
        defaults = {
            "is_setup": False,
            "text-editor": "",
            "root-path":"",
            "banner-font":"ansi_regular",
            "banner-color":"red",

            "projects": {},
        }
        json.dump(defaults, f, indent=4)
except FileExistsError:
    pass

editors_available = [
    "Vim",
    "GNU Nano",
    "GNU Emacs",
    "Visual Studio Code",
    "PyCharm",
    "Sublime Text",
    "Atom",
    "Other",
]

languages_supported = [
    "Python",
    "C++",
    "C#",
    "Java",
    "Go",
    "Rust",
    "Node.js",
    "TypeScript",
    "Web",
    "Other",
]

def save_to_json(config):   
    try:
        with open(CONFIG_FILE, "r") as f: 
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or corrupted file
        data = {}

    data.update(config)

    with open(CONFIG_FILE, "w") as f:  
        json.dump(data, f, indent=4)
