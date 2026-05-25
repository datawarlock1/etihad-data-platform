import os
from typing import Dict


def load_config() -> Dict[str, str]:
    """Load configuration from environment variables.

    This minimal loader keeps secrets out of source code and allows CI
    to inject credentials as environment variables.
    """
    return {
        "DB_PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "STORAGE_KEY": os.environ.get("STORAGE_KEY", ""),
        "ENV": os.environ.get("ENV", "dev"),
    }
