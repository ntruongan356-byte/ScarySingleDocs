import os
import sys
from pathlib import Path
from unittest.mock import MagicMock
import importlib.util

# --- Mock google.colab ---
# This must be done before any other imports that might try to import google.colab
google_colab = MagicMock()
google_colab.output = MagicMock()
google_colab.output.register_callback = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.colab'] = google_colab


# --- Add project directories to Python path ---
CWD = Path.cwd()

def run_widget_test():
    """Run the widget test."""
    print("Importing and running widgets-en.py...")
    try:
        # Add project directories to Python path
        sys.path.append(str(CWD / 'modules'))
        sys.path.append(str(CWD / 'scripts'))
        
        # Define the path to the module
        widgets_path = CWD / 'scripts' / 'en' / 'widgets-en.py'
        
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