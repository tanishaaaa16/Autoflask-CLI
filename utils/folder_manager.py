import os

def create_project_directory(project_location, project_name):
    """Create the project directory and return the full path"""
    full_project_path = os.path.join(project_location, project_name)
    
    print("Creating project directory...")
    try:
        os.makedirs(full_project_path, exist_ok=True)
        return full_project_path
    except OSError as e:
        print(f"Failed to create project directory: {e}")
        return None
        
def navigate_to_directory(directory_path):
    """Change the current directory to the specified path"""
    try:
        os.chdir(directory_path)
        return True
    except OSError as e:
        print(f"Failed to navigate to directory: {e}")
        return False

def create_project_structure(project_name, project_cat):
    """Create the basic project structure based on project category"""
    print("Creating project structure...")
    try:
        # Standard directories for all projects
        os.makedirs('templates', exist_ok=True)
        os.makedirs('static/css', exist_ok=True)
        os.makedirs('static/js', exist_ok=True)
        
        # Additional directories for ML projects
        if project_cat == "Machine Learning":
            print("Creating structured ML project directories...")
            os.makedirs('data/raw', exist_ok=True)
            os.makedirs('data/processed', exist_ok=True)
            os.makedirs('models', exist_ok=True)
            os.makedirs('notebooks', exist_ok=True)
            os.makedirs('scripts', exist_ok=True)
            
            with open('notebooks/FirstNotebook.ipynb', 'w') as f:
                f.write('{\n "cells": [],\n "metadata": {},\n "nbformat": 4,\n "nbformat_minor": 5\n}')
                
            with open('models/model.py', 'w') as f:
                f.write("# Your model definition here")
        
        # Create standard files
        with open('.gitignore', 'w') as f:
            f.write("""# Byte-compiled / optimized / DLL files
__pycache__/
*.pyc
*.pyo
*.pyd
# Environments
.env
venv/
ENV/
# Distribution / packaging
dist/
build/
data/
*.egg-info/
# Log files
*.log
# Unit test / coverage reports
htmlcov/
.tox/
.coverage
# Jupyter Notebook
.ipynb_checkpoints/
# OS generated files #
.DS_Store
Thumbs.db
""")

        with open('README.md', 'w') as f:
            f.write(f"""# {project_name}

A brief description of the project.

## Installation

Instructions on how to install and run the project.

## Usage

Examples of how to use the project.

## Contributing

Guidelines for contributing to the project.
""")

        # Create project type identifier file
        with open('project_type.txt', 'w') as f:
            f.write(project_cat)
            
        return True
    except OSError as e:
        print(f"Failed to create project structure: {e}")
        return False

def create_app_py(has_auth=False):
    """Create the app.py file based on authentication needs"""
    print("Creating app.py...")
    try:
        if not has_auth:
            with open('app.py', 'w') as f:
                f.write("""from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
""")
        return True
    except OSError as e:
        print(f"Failed to create app.py: {e}")
        return False

def create_requirements_file(selected_libs, auth_libs=None):
    """Create requirements.txt with selected libraries"""
    print("Creating requirements.txt...")
    try:
        with open('requirements.txt', 'w') as f:
            f.write("flask\n")
            if selected_libs:
                f.write('\n'.join(selected_libs) + '\n')
            if auth_libs:
                f.write('\n'.join(auth_libs) + '\n')
        return True
    except OSError as e:
        print(f"Failed to create requirements.txt: {e}")
        return False
    
    
    
if __name__ == "__main__":
    # Example usage
    project_location = os.getcwd()
    project_name = "Demo"
    project_cat = "Web Development"
    
    full_project_path = create_project_directory(project_location, project_name)
    
    if not full_project_path:
        print("Failed to create project directory.")
        exit(1)
    
    if not navigate_to_directory(full_project_path):
        print("Failed to navigate to project directory.")
        exit(1)
    
    if not create_project_structure(project_name, project_cat):
        print("Failed to create project structure.")
        exit(1)
    
    if not create_app_py():
        print("Failed to create app.py.")
        exit(1)
    
    if not create_requirements_file(["flask"]):
        print("Failed to create requirements.txt.")
        exit(1)