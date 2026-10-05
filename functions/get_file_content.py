import os

from openai.types.chat import ChatCompletionFunctionToolParam

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
    except Exception as e: #noqa: BLE001
        return f"Error: {e}"

schema_get_file_content: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Provides the content of the given file in the working directory, in the provided filepath",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The filepath for the file that is gonna read, relative to working directory (default is the working directory itself)"
                }
            },
            "required": [
                "file_path",
            ]
        }
    }
}
