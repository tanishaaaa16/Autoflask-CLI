import os
from .folder_manager import create_project_directory, navigate_to_directory, create_project_structure, create_app_py, create_requirements_file
from .lib_manager import setup_virtual_environment, install_libraries, get_auth_libs
from .template_manager import create_css_templates
from .auth_manager import setup_authentication

def setup_project(create_venv, project_name, project_cat, additional_libs, install_libs, 
                  project_location, css_framework, add_auth, selected_libs):
    """Sets up the project with specified parameters."""

    # Create the project directory
    full_project_path = create_project_directory(project_location, project_name)
    if not full_project_path:
        return
    
    # Navigate to project directory
    if not navigate_to_directory(full_project_path):
        os.chdir(project_location)  # Go back if navigation failed
        return
    
    pip_executable = 'pip'  # Default to system pip
    
    # Set up virtual environment if requested
    if create_venv:
        pip_executable = setup_virtual_environment(full_project_path)
        if not pip_executable:
            os.chdir(project_location)
            return
    
    # Install Flask and essential libraries
    essential_libs = ["flask"]
    auth_libs = []
    
    if add_auth:
        auth_libs = get_auth_libs()
        essential_libs.extend(auth_libs)
    
    if install_libs:
        print("Installing Flask and essential libraries...")
        if not install_libraries(pip_executable, essential_libs, full_project_path):
            os.chdir(project_location)
            return
        
        # Install selected libraries
        if selected_libs:
            if not install_libraries(pip_executable, selected_libs, full_project_path):
                os.chdir(project_location)
                return
    else:
        print("Skipping library installation (Install libs option is disabled).")
    
    # Create project structure
    if not create_project_structure(project_name, project_cat):
        os.chdir(project_location)
        return
    
    # Create CSS templates
    if not create_css_templates(css_framework, project_name):
        os.chdir(project_location)
        return
    
    # Set up authentication if requested
    if add_auth:
        if not setup_authentication(project_name):
            os.chdir(project_location)
            return
    else:
        # Create simple app.py if no auth
        if not create_app_py(False):
            os.chdir(project_location)
            return
    
    # Create requirements.txt file
    if not create_requirements_file(selected_libs, auth_libs if add_auth else None):
        os.chdir(project_location)
        return
    
    print("Project setup complete!")
    print(f"Project '{project_name}' setup complete at '{full_project_path}'!")
    
    # Go back to original directory
    os.chdir(project_location)
    
    
    
    
    
if __name__ == "__main__":
    # Example usage
    setup_project(
        create_venv=False,
        project_name="MyFlaskApp",
        project_cat="Machine Learning",
        additional_libs=["numpy", "pandas"],
        install_libs=False,
        project_location=os.getcwd(),
        css_framework="Tailwind",
        add_auth=True,
        selected_libs=["requests"]
    )