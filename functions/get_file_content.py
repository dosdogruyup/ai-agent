import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))

        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(file_path_abs) as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string = file_content_string + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return f"Success!\n\n{file_content_string}"
    except Exception as e:
        return f"Error: {e}"
