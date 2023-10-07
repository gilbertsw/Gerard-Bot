from pathlib import Path

def _read_file(path: str) -> str:
    with open(path,'r') as f:
        return f.readlines()

def get_help():
    return _read_file("txt\help.txt")

def get_persona():
    return _read_file("txt\persona.txt")

def get_main_prompt():
    return _read_file("txt\main_prompt.txt")