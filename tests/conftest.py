"""Pytest configuration and fixtures."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


@pytest.fixture
def sample_dataframe():
    """Provide sample DataFrame for testing."""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [10, 20, 30, 40, 50],
        'feature3': ['A', 'B', 'A', 'B', 'A'],
        'target': [0, 1, 0, 1, 0]
    })


@pytest.fixture
def sample_dataframe_with_missing():
    """Provide DataFrame with missing values."""
    return pd.DataFrame({
        'feature1': [1, 2, np.nan, 4, 5],
        'feature2': [10, np.nan, 30, 40, 50],
        'feature3': ['A', 'B', None, 'B', 'A'],
        'target': [0, 1, 0, 1, 0]
    })


@pytest.fixture
def temp_data_file(tmp_path, sample_dataframe):
    """Create temporary CSV file."""
    file_path = tmp_path / "test_data.csv"
    sample_dataframe.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def mock_config():
    """Provide mock configuration."""
    return {
        'model': {
            'type': 'random_forest',
            'n_estimators': 100,
            'random_state': 42
        },
        'preprocessing': {
            'handle_missing': 'drop',
            'scale_features': True
        }
    }
