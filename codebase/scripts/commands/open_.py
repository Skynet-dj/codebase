import json
import subprocess
from codebase.scripts.com_util import CONFIG_FILE,  text_editor_command


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)["text-editor-command"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return text_editor_command



def open_project(path: str) -> None:
    command = load_config()
    subprocess.run(f"{command} {path}", shell=True)
    return

def open_template(path: str) -> None:
    command = load_config()
    subprocess.run(f"{command} {path}", shell=True)
    return

def open_explorer(path: str, ) -> None:
    command = load_config()
    subprocess.run(f"explorer {path}", shell=True)
    return
