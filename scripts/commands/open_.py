import json
import subprocess
from scripts.com_util import CONFIG_FILE, text_editor, text_editor_command

try:
    with open(CONFIG_FILE, "r") as f:
        command = json.load(f)["text-editor-command"]
except (FileNotFoundError, json.JSONDecodeError) as e:
    command = text_editor_command



def open_project(path: str) -> None:
    subprocess.call(f"{command} {path}", shell=True)
    return

def open_template(path: str) -> None:
    subprocess.call(f"{command} {path}", shell=True)
    return

def open_explorer(path: str, ) -> None:
    subprocess.call(f"explorer {path}", shell=True)
    return
