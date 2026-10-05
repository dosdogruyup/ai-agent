import json
from collections.abc import Callable

from openai.types.chat import ChatCompletionToolUnionParam

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions: list[ChatCompletionToolUnionParam] = [
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if not function_name in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }
    else:
        result = function_map[function_name]("./calculator", **function_args)
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        }
