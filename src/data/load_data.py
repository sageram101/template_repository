"""Data loading utilities."""

from pathlib import Path
from typing import Union

import pandas as pd
from loguru import logger


def load_csv(
    filepath: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """
    Load data from CSV file.

    Args:
        filepath: Path to CSV file
        **kwargs: Additional arguments for pd.read_csv

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If file is empty
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    logger.info(f"Loading data from {filepath}")

    try:
        df = pd.read_csv(filepath, **kwargs)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df
    except pd.errors.EmptyDataError:
        logger.error(f"File is empty: {filepath}")
        raise


def load_excel(
    filepath: Union[str, Path],
    sheet_name: Union[str, int] = 0,
    **kwargs
) -> pd.DataFrame:
    """
    Load data from Excel file.

    Args:
        filepath: Path to Excel file
        sheet_name: Sheet name or index
        **kwargs: Additional arguments for pd.read_excel

    Returns:
        Loaded DataFrame
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    logger.info(f"Loading data from {filepath}, sheet: {sheet_name}")

    df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

    return df


def load_parquet(
    filepath: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """
    Load data from Parquet file.

    Args:
        filepath: Path to Parquet file
        **kwargs: Additional arguments for pd.read_parquet

    Returns:
        Loaded DataFrame
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    logger.info(f"Loading data from {filepath}")

    df = pd.read_parquet(filepath, **kwargs)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

    return df


def save_data(
    df: pd.DataFrame,
    filepath: Union[str, Path],
    format: str = "csv",
    **kwargs
) -> None:
    """
    Save DataFrame to file.

    Args:
        df: DataFrame to save
        filepath: Output file path
        format: File format ('csv', 'parquet', 'excel')
        **kwargs: Additional arguments for save function
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Saving data to {filepath}")

    if format == "csv":
        df.to_csv(filepath, index=False, **kwargs)
    elif format == "parquet":
        df.to_parquet(filepath, index=False, **kwargs)
    elif format == "excel":
        df.to_excel(filepath, index=False, **kwargs)
    else:
        raise ValueError(f"Unsupported format: {format}")

    logger.info(f"Data saved successfully")
