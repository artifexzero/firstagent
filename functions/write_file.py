import os
from google.genai import types

def write_file(working_directory, file_path, file_content_string):
    
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(abs_working_dir):
            os.makedirs(abs_working_dir)

        with open(target_file, "w") as f:
            f.write(file_content_string)

        return f'Successfully wrote to "{target_file}" ({len(file_content_string)} characters written)'

    except Exception as e:
        print(f'Error writing file {target_file}: {e}')
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a string to the specified file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read a file from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "file_content_string": types.Schema(
                type=types.Type.STRING,
                description="The string to be written to the file.",
            )
        }
    )
)
