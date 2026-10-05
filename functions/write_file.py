import os

from openai.types.chat import ChatCompletionFunctionToolParam


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
            with open(file_path_abs, "w") as f:
                return f'Successfully wrote to "{file_path}" ({f.write(content)} characters written)'
    except Exception as e: #noqa: BLE001
        return f"Error: {e}"

schema_write_file: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the provided characters into the provided file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath for the file that is gonna be written to, relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "The content that is gonna be written into the file"
                }
            },
            "required": [
                "file_path",
                "content",
            ]
        }
    }
}
