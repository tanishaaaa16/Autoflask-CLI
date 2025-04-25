import os
import argparse
from lib_manager import category_libs
from setup_project import setup_project


def main():
    print("Welcome to AutoFlask!")
    parser = argparse.ArgumentParser(description="Create a new Flask project.")
    parser.add_argument("name", help="Name of the project")
    
    venv_group = parser.add_mutually_exclusive_group()
    venv_group.add_argument("--venv-true", action="store_true", dest="create_venv", help="Create a virtual environment")
    venv_group.add_argument("--venv-false", action="store_false", dest="create_venv", help="Do not create a virtual environment")
    parser.set_defaults(create_venv=None)
    
    parser.add_argument(
        "--cat",
        help="Category of project (Web Development, Machine Learning, etc.)",
    )
    parser.add_argument(
        "--libs", help="Additional libraries to install (comma-separated)",
    )

    install_group = parser.add_mutually_exclusive_group()
    install_group.add_argument("--install-true", action="store_true", dest="install_libs", help="Install selected libraries")
    install_group.add_argument("--install-false", action="store_false", dest="install_libs", help="Do not install selected libraries")
    parser.set_defaults(install_libs=None)
    
    parser.add_argument(
        "--location",
        help="Project location (defaults to current directory)",
        default=os.getcwd(),
    )

    parser.add_argument("--auth", action="store_true", help="Include Flask Authentication")

    css_group = parser.add_mutually_exclusive_group(required=False)
    css_group.add_argument("--css-tailwind", action="store_const", const="Tailwind", dest="css", help="Use Tailwind CSS")
    css_group.add_argument("--css-bootstrap", action="store_const", const="Bootstrap", dest="css", help="Use Bootstrap CSS")
    css_group.add_argument("--css-none", action="store_const", const="None", dest="css", help="Do not use any CSS framework")

    args = parser.parse_args()

    project_name = args.name
    project_location = args.location
    project_cat = args.cat
    additional_libs = args.libs
    css_framework = args.css if args.css else "None"  # Default to None if no CSS argument
    add_auth = args.auth
    selected_libs = []

    # Check if any arguments other than 'name' and 'location' were provided
    if any([args.cat, args.libs, (args.install_libs is not None), args.auth, args.css, (args.create_venv is not None)]):
        # Use the values provided in the arguments
        if args.create_venv is None:
            create_venv = input("Create a virtual environment? (y/n): ").lower() == 'y'
        else:
            create_venv = args.create_venv
            
        if not project_cat:
           project_types = list(category_libs.keys())
           print("Available project categories:")
           for i, p_cat in enumerate(project_types):
               print(f"{i+1}. {p_cat}")

           while True:
               try:
                   choice = int(input("Select project category (enter number): "))
                   if 1 <= choice <= len(project_types):
                       project_cat = project_types[choice - 1]
                       break
                   else:
                       print("Invalid choice. Please select a number from the list.")
               except ValueError:
                   print("Invalid input. Please enter a number.")
                   
        if not additional_libs:
            additional_libs = input("Enter additional libraries (comma-separated, or leave blank): ")
           
        if not add_auth:
             add_auth_choice = input("Include Flask Authentication? (y/n): ").lower()
             add_auth = add_auth_choice == 'y'

        if args.install_libs is None:
            install_libs_choice = input("Install all selected libraries? (y/n): ").lower()
            install_libs = install_libs_choice == 'y'
        else:
            install_libs = args.install_libs

        libraries = category_libs.get(project_cat, [])
        if libraries and install_libs:
            print(f"Available libraries for {project_cat}: {', '.join(libraries)}")
            for lib in libraries:
                choice = input(f"Install {lib}? (y/n): ").lower()
                if choice == 'y':
                    selected_libs.append(lib)

        if additional_libs and install_libs:
            extra_libs = additional_libs.split(',')
            print(f"Available libraries for additionalLibs: {', '.join(extra_libs)}")
            for lib in extra_libs:
                choice = input(f"Install {lib}? (y/n): ").lower()
                if choice == 'y':
                    selected_libs.append(lib)

    else:
        create_venv = input("Create a virtual environment? (y/n): ").lower() == 'y'
        # Prompt for all information
        project_cats = list(category_libs.keys())
        print("Available project categories:")
        for i, p_cat in enumerate(project_cats):
            print(f"{i+1}. {p_cat}")

        while True:
            try:
                choice = int(input("Select project category (enter number): "))
                if 1 <= choice <= len(project_cats):
                    project_cat = project_cats[choice - 1]
                    break
                else:
                    print("Invalid choice. Please select a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        additional_libs = input("Enter additional libraries (comma-separated, or leave blank): ")
        
        if args.install_libs is None:
            install_libs_choice = input("Install all selected libraries? (y/n): ").lower()
            install_libs = install_libs_choice == 'y'
        else:
            install_libs = args.install_libs
            
        if install_libs:
            libraries = category_libs.get(project_cat, [])
            if libraries:
                print(f"Available libraries for {project_cat}: {', '.join(libraries)}")
                for lib in libraries:
                    choice = input(f"Install {lib}? (y/n): ").lower()
                    if choice == 'y':
                        selected_libs.append(lib)

            if additional_libs:
                extra_libs = additional_libs.split(',')
                print(f"Available libraries for additionalLibs: {', '.join(extra_libs)}")
                for lib in extra_libs:
                    choice = input(f"Install {lib}? (y/n): ").lower()
                    if choice == 'y':
                        selected_libs.append(lib)
                        
        add_auth_choice = input("Include Flask Authentication? (y/n): ").lower()
        add_auth = add_auth_choice == 'y'
        
    # Check if CSS framework was explicitly set through arguments before prompting
    if args.css is None:
      css_frameworks = ["None", "Bootstrap", "Tailwind"]
      print("Available CSS frameworks:")
      for i, framework in enumerate(css_frameworks):
          print(f"{i+1}. {framework}")
      while True:
          try:
              choice = int(input("Select CSS framework (enter number): "))
              if 1 <= choice <= len(css_frameworks):
                  css_framework = css_frameworks[choice - 1]
                  break
              else:
                  print("Invalid choice. Please select a number from the list.")
          except ValueError:
              print("Invalid input. Please enter a number.")

    setup_project(
        create_venv,
        project_name,
        project_cat,
        additional_libs,
        install_libs,
        project_location,
        css_framework,
        add_auth,
        selected_libs
    )
    
if __name__ == "__main__":
    main()