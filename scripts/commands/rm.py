import os

def rm_project(path: str) -> None:
    os.remove(path)
    return True

def rm_template(path):
    os.remove(path)