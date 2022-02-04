import os
from string import whitespace as WHITESPACE

def try_remove_file(path: str) -> None:
    try:
        os.unlink(path)
    except OSError:
        if os.path.exists(path):
            print(f'Error: could not unlink file at path {path}')

def remove_whitespace(string: str) -> str:
    return string.translate(str.maketrans('', '', WHITESPACE))
