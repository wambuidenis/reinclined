import os
import json
from glob import iglob
import re
import sys

DIR_SEPARATOR = os.path.sep


def safe_mkdirs(path):
    """
    This makes new directories if needed.

    Args:
        path (str): The full path of the would be directory.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def make_json(content, path, append=False, ensure_ascii=False):
    """
    This writes a dictionary to a json file.

    Args:
        content (dict): The content to write.
        path (str): The path to write to.
        append (bool): Whether to append data to an existing json.
        ensure_ascii (bool): Whether to contain ASCII characters.
    """
    if append and os.path.exists(path):
        stored_json = load_json(path)
        content = {**stored_json, **content}

    safe_mkdirs(DIR_SEPARATOR.join(path.split(DIR_SEPARATOR)[:-1]))
    with open(path, 'w') as fp:
        json.dump(content, fp, indent=4, ensure_ascii=ensure_ascii)


def load_json(path):
    """
    This reads and loads json into python from a file.

    Args:
        path (str): The path to read from.

    Returns:
        data (dict): The json data.
    """
    if not os.path.exists(path):
        return {}
    with open(path) as fp:
        return json.load(fp)


def find_reference_in_list(name, references):
    """
    This finds the matching reference (file path) in a list of references.

    Args:
        name (str): The name of the file to look for.
        references (list): The list of references to look through for a match.

    Returns:
        reference (str): The matching reference from the list.
    """
    return next((ref for ref in references if name == ref.split(DIR_SEPARATOR)[-1]), 0)



def get_root_dir():
    """
    This gets the root directory by looking for .git.

    Returns:
        root_dir (str): The root dir of the project.
    """
    cwd = os.getcwd().split(DIR_SEPARATOR)
    path = ''
    for index, p in enumerate(cwd):
        if p:
            if sys.platform == "win32" and index == 0:
                path += f'{p}'
            else:
                path += f'{DIR_SEPARATOR}{p}'
            if os.path.isdir(path) and 'Pipfile' in os.listdir(path):
                return path


def get_src_app_dir():
    """
    This finds which src app directory (app, map, ..) we're automating against.

    Returns:
        app (str): The src app/project folder in use.
    """
    return os.environ.get('PYTEST_CURRENT_TEST').split('::')[0].split('/')[1]


def expand_directory(path):
    """
    This expands a directory into a list of its files absolute paths.

    Args:
        path (str): The path of the directory to traverse.

    Returns:
        files (list): The list of files in a directory.
    """
    files = [path]
    if os.path.isdir(path):
        files = [f for f in iglob(f'{path}{DIR_SEPARATOR}{DIR_SEPARATOR}**', recursive=True) if
                 'ds_store' not in f.lower()]
    return files

def is_mac(test_string: str) -> str:
    """
    This will make the path names uniform from platform to platform.

    Args:
        test_string (str): The current platform name.

    Returns:
        uniformed (str): Uniform platform name.
    """
    platform = sys.platform
    if platform == "darwin":
        pattern = '^Mac'
        result = re.match(pattern, test_string, re.IGNORECASE)
        uniformed = "macos" if result else result
    elif platform == "win32":
        pattern = '^Win'
        result = re.match(pattern, test_string, re.IGNORECASE)
        uniformed = "windows" if result else result
    else:
        pattern = '^Lin'
        result = re.match(pattern, test_string, re.IGNORECASE)
        uniformed = "linux" if result else result
    return uniformed
