import os
import subprocess
import sys

category_libs = {
    "Web Development": ["flask-wtf", "flask-bootstrap", "flask-login", "flask-mail", "flask-migrate", "flask-restful"],
    "Image Processing": ["opencv-python", "Pillow", "scikit-image", "imageio", "tesseract", "pyzbar"],
    "Machine Learning": ["numpy", "pandas", "scikit-learn", "tensorflow", "torch", "xgboost", "lightgbm", "catboost"],
    "NLP": ["spacy", "nltk", "transformers", "gensim", "textblob", "sentence-transformers"],
    "Data Analysis": ["pandas", "matplotlib", "seaborn", "plotly", "statsmodels"],
    "Web Scraping": ["beautifulsoup4", "scrapy", "selenium", "requests", "httpx", "dputils"],
    "Computer Vision": ["opencv-python", "mediapipe", "face_recognition", "dlib"],
    "Visualization": ["plotly", "dash", "bokeh", "altair", "streamlit", "matplotlib", "seaborn", "numpy", "pandas"],
    "Database": ["sqlalchemy", "pymongo", "psycopg2", "mysql-connector-python"],
    "Audio Processing": ["pydub", "librosa", "soundfile", "audioread"],
    "Desktop GUI": ["pywebview","flask-wtf", "flask-bootstrap", "flask-login", "flask-mail", "flask-migrate", "flask-restful"],
}

def get_auth_libs():
    """Return libraries needed for authentication"""
    return ["flask-sqlalchemy", "flask-login", "bcrypt"]

def setup_virtual_environment(project_path):
    """Create and activate a virtual environment"""
    print("Creating virtual environment...")
    try:
        # Create virtual environment
        result = subprocess.run([sys.executable, '-m', 'venv', 'venv'], 
                                check=True, capture_output=True, text=True, 
                                cwd=project_path)
        print(result.stdout)
        print(result.stderr)
        print("Virtual environment created successfully.")
        
        # Determine pip path based on OS
        if os.name == 'nt':
            activate_script = os.path.join("venv", "Scripts", "python.exe")  # Windows
            pip_executable = os.path.join('venv', 'Scripts', 'pip')
        else:
            activate_script = os.path.join("venv", "bin", "python")  # Linux/Mac
            pip_executable = os.path.join('venv', 'bin', 'pip')
            
        # Upgrade pip
        print("Upgrading pip...")
        result = subprocess.run([os.path.join(project_path, activate_script), 
                                '-m', 'pip', 'install', '--upgrade', 'pip'], 
                                check=True, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        print("Pip upgraded successfully.")
        
        return pip_executable
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment: {e.stderr}")
        return None

def install_libraries(pip_path, libraries, project_path):
    """Install specified libraries"""
    if not libraries:
        return True
        
    print(f"Installing libraries: {', '.join(libraries)}...")
    try:
        result = subprocess.run([pip_path, 'install'] + libraries, 
                              check=True, capture_output=True, text=True,
                              cwd=project_path)
        print(result.stdout)
        print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install libraries: {e.stderr}")
        return False
    
    