import json
import os
from scripts.com_util import CONFIG_FILE, text_editor, text_editor_command

try:
    with open(CONFIG_FILE, "r") as f:
        command = json.load(f)["text-editor-command"]
except (FileNotFoundError, json.JSONDecodeError) as e:
    command = text_editor_command



def open_project(path: str) -> None:
    os.system(f"{command} {path}")
    return

def open_template(path: str) -> None:
    os.system(f"{command} {path}")
    return

def open_explorer(path: str) -> None:
    os.system(f"explorer {path}")
    return