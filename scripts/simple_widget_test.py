import os
from pathlib import Path
import sys
import importlib.util

# Add modules directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / 'modules'))

# --- Environment Setup ---
# This needs to be done at the module level before any of the script's
# modules are imported.
print("Setting up environment...")
cwd = Path.cwd()
home_path = cwd
scr_path = home_path / 'ScarySingleDocs'
settings_path = scr_path / 'settings.json'
venv_path = home_path / 'venv'

# Create the settings directory if it doesn't exist
settings_path.parent.mkdir(exist_ok=True)

# Create a dummy settings.json if it doesn't exist
if not settings_path.exists():
    with open(settings_path, 'w') as f:
        f.write('{"ENVIRONMENT": {"env_name": "local"}}')

# Set environment variables
os.environ['home_path'] = str(home_path)
os.environ['scr_path'] = str(scr_path)
os.environ['settings_path'] = str(settings_path)
os.environ['venv_path'] = str(venv_path)
print("Environment setup complete.")
# --- End Environment Setup ---

def run_widget_test():
    """Run the widget test."""
    print("Importing and running widgets-en.py...")
    try:
        # Define the path to the module
        widgets_path = Path(__file__).parent / 'en' / 'widgets-en.py'
        
        # Create a module spec
        spec = importlib.util.spec_from_file_location("widgets_en", widgets_path)
        
        # Create a new module based on the spec
        widgets_script = importlib.util.module_from_spec(spec)
        
        # Execute the module
        spec.loader.exec_module(widgets_script)
        
        print("Widgets script executed successfully.")
    except Exception as e:
        print(f"An error occurred while running the widgets script: {e}")

if __name__ == "__main__":
    run_widget_test()