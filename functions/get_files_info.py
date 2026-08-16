import os
from collections.abc import Callable
from typing import Any

def format_text(file: str, target_dir: str):
    try:
        full_path = os.path.join(target_dir, file)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        file_size = os.path.getsize(full_path)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        is_dir = os.path.isdir(full_path)
    except Exception as e:
        return f"Error: {e}"
    
    return f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"

    try:
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    except Exception as e:
        return f"Error: {e}"
    
    if (os.path.commonpath([working_dir_abs, target_dir])) != working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not  os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    else:
        return (f'{"\n".join([format_text(file, target_dir) for file in os.listdir(target_dir)])}')
            
        
        
    
    
