import os
import subprocess

from openai.types.chat import ChatCompletionFunctionToolParam


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", file_path_abs]
            if args:
                command.extend(args)
            completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30, check=False)

            result = ""

            if completed_process.returncode:
                result += f"Process exited with code {completed_process.returncode}\n"

            if not completed_process.stdout and not completed_process.stderr:
                result += "No output produced\n"
            else:
                if completed_process.stdout:
                    result += f"STDOUT: {completed_process.stdout}\n"
                if completed_process.stderr:
                    result += f"STDERR: {completed_process.stderr}\n"

            return result

    except Exception as e: #noqa: BLE001
        return f"Error: executing Python file: {e}"

schema_run_python_file: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the python file that is at the provided path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath for the Python file to run, relative to the working directory"
                },
                "args": {
                    "type": "array",
                    "description": "A list of arguments to run the Python file with"
                }
            },
            "required": [
                "file_path"
            ]
        }
    }
}
