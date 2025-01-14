import json
import subprocess
from ..com_util import CONFIG_FILE,  text_editor_command


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)["text-editor-command"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return text_editor_command


def open__(path: str, exp: bool=False) -> None:
    command = load_config()
    if exp:
        command = "explorer"        
    subprocess.run(f"{command} {path}", shell=True)
    return