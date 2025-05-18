# src/config.py
import os

# Get absolute path to src/
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to maps directory (inside src/)
MAPS_DIR = os.path.join(SRC_DIR, "maps")

# Create it if it doesn't exist
os.makedirs(MAPS_DIR, exist_ok=True)
