"""
Test configuration for FilesystemWatcher Phase 1
"""
from pathlib import Path

# VAULT_PATH: Absolute path to the AI_Employee_Vault
VAULT_PATH = Path(r"C:\Users\User\Desktop\hakathon-00\AI_Employee_Vault")

# WATCH_DIRECTORY: Directory to monitor for file drops
# For Windows testing, using a temp directory
WATCH_DIRECTORY = Path(r"C:\Users\User\Desktop\hakathon-00\test_drop_folder")

# CHECK_INTERVAL: How often to check for new files (seconds)
CHECK_INTERVAL = 60

# Ensure directories exist
WATCH_DIRECTORY.mkdir(parents=True, exist_ok=True)
VAULT_PATH.joinpath("Needs_Action").mkdir(parents=True, exist_ok=True)
