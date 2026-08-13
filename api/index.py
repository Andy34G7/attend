import sys
from pathlib import Path

# Add project root directory to path for clean imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
