#!/usr/bin/env python3

import os

# Define the base directory
BASE_DIR = "synthea-maternity-research"

# Define subdirectories and files to create
structure = {
    "synthea-custom": [
        "obstetrics_module.json",
        "custom_fields_config.json"
    ],
    "data": [],
    "scripts": [
        "data_ingestion.py",
        "feature_engineering.py",
        "clustering.py",
        "narrative_generator.py"
    ],
    "notebooks": [],
    "reports": [],
    ".github": [
        "workflows/ci-cd.yml"
    ]
}

# Files that live directly under the BASE_DIR
top_level_files = [
    "environment.yml"
]

def make_dirs_and_files():
    # 1. Create the base directory
    os.makedirs(BASE_DIR, exist_ok=True)

    # 2. Create top-level files inside the base directory
    for filename in top_level_files:
        file_path = os.path.join(BASE_DIR, filename)
        create_file(file_path, content=f"# Placeholder for {filename}\n")

    # 3. Create subdirectories and their files
    for folder_name, file_list in structure.items():
        # Build the subdirectory path
        subdir_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(subdir_path, exist_ok=True)

        for file_info in file_list:
            if "/" in file_info:
                # Handle nested directories, e.g. "workflows/ci-cd.yml"
                nested_dir, nested_file = file_info.split("/", 1)
                nested_path = os.path.join(subdir_path, nested_dir)
                os.makedirs(nested_path, exist_ok=True)

                # Create the file inside the nested directory
                file_path = os.path.join(nested_path, nested_file)
                create_file(file_path, content=f"# Placeholder for {nested_file}\n")
            else:
                # Just a file in the current subdirectory
                file_path = os.path.join(subdir_path, file_info)
                create_file(file_path, content=f"# Placeholder for {file_info}\n")

def create_file(path, content=""):
    """Create a file at the given path with optional content."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    make_dirs_and_files()
    print(f"Project structure created under '{BASE_DIR}'.")
