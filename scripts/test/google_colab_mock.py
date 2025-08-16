from unittest.mock import MagicMock
import sys

# Create a mock for the 'google.colab' module
google_colab = MagicMock()

# Mock the 'output' object and its 'register_callback' method
google_colab.output = MagicMock()
google_colab.output.register_callback = MagicMock()

# Add the mock to sys.modules
sys.modules['google'] = MagicMock()
sys.modules['google.colab'] = google_colab