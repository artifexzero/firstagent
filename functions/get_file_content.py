import os
from functions.config import *
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}'
    
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(FILE_CHAR_LIMIT)
    
        if len(file_content_string) == FILE_CHAR_LIMIT:
            file_append = f'[...File "{target_file}" truncated at {FILE_CHAR_LIMIT} characters]'
            file_content_string = file_content_string + file_append
        
        return file_content_string

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Gets contents of a file and returns a string truncated at {FILE_CHAR_LIMIT}, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        }
    )
)