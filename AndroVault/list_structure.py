import os
from typing import List
import sys

def list_directory_structure(root_path: str, indent: str = "", output: List[str] = None) -> List[str]:
    """Lists directory structure excluding __pycache__ and venv"""
    if output is None:
        output = []
    
    try:
        # Get and sort directory contents
        items = sorted(os.listdir(root_path))
    except PermissionError:
        return output

    for item in items:
        # Skip __pycache__ and venv
        if item == "__pycache__" or item == "venv":
            continue
            
        full_path = os.path.join(root_path, item)
        
        if os.path.isdir(full_path):
            # Print directories with trailing slash
            print(f"{indent}├── {item}/")
            # Recurse into subdirectories
            list_directory_structure(full_path, indent + "│   ", output)
        else:
            # Print files
            print(f"{indent}├── {item}")
    
    return output

if __name__ == "__main__":
    # Get the password_manager directory path
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        # Use current directory if no path provided
        root_dir = os.getcwd()
    
    # Print the root directory name
    print(f"{os.path.basename(root_dir)}/")
    
    # Print the directory structure
    list_directory_structure(root_dir)
    