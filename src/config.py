```python
"""Configuration management for the project."""

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models"
CONFIG_DIR = ROOT_DIR / "configs"


class Config:
    """Application configuration."""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path or CONFIG_DIR / "config.yaml"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key (supports nested keys with dots)
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value is not None else default


# Global configuration instance
config = Config()


# Path configurations
class Paths:
    """Project paths."""

    ROOT = ROOT_DIR
    DATA = DATA_DIR
    RAW_DATA = DATA_DIR / "raw"
    INTERIM_DATA = DATA_DIR / "interim"
    PROCESSED_DATA = DATA_DIR / "processed"
    EXTERNAL_DATA = DATA_DIR / "external"
    MODELS = MODEL_DIR
    TRAINED_MODELS = MODEL_DIR / "trained"
    REPORTS = ROOT_DIR / "reports"
    FIGURES = ROOT_DIR / "reports" / "figures"


# Ensure directories exist
for path in [
    Paths.RAW_DATA,
    Paths.INTERIM_DATA,
    Paths.PROCESSED_DATA,
    Paths.EXTERNAL_DATA,
    Paths.TRAINED_MODELS,
    Paths.FIGURES,
]:
    path.mkdir(parents=True, exist_ok=True)
