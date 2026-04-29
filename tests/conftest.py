import os
import sys
from pathlib import Path

# Ensure `app/` modules are importable as top-level packages (api, core, models, ...).
APP_DIR = Path(__file__).resolve().parent.parent / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Tests must not require a real database/secrets file.
os.environ.setdefault("APP_ENV_FILE", "/dev/null")
os.environ.setdefault("AUTO_CREATE_TABLES", "false")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
