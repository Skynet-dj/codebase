import os
from codebase.scripts.com_util import update_project

def rm_project(path, name) -> None:
    update_project(path, name,True)
    os.remove(path)
    return True

def rm_template(path):
    os.remove(path)