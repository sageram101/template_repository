"""Data preprocessing utilities."""

from typing import List, Optional, Union

import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split


class DataPreprocessor:
    """Data preprocessing pipeline."""

    def __init__(self):
        """Initialize preprocessor."""
        self.column_mapping = {}
        self.numeric_columns = []
        self.categorical_columns = []

    def clean_data(
        self,
        df: pd.DataFrame,
        drop_duplicates: bool = True,
        handle_missing: str = "drop"
    ) -> pd.DataFrame:
        """
        Clean DataFrame.

        Args:
            df: Input DataFrame
            drop_duplicates: Whether to drop duplicate rows
            handle_missing: How to handle missing values ('drop', 'fill')

        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning data...")

        df = df.copy()

        # Drop duplicates
        if drop_duplicates:
            initial_rows = len(df)
            df = df.drop_duplicates()
            logger.info(f"Dropped {initial_rows - len(df)} duplicate rows")

        # Handle missing values
        if handle_missing == "drop":
            initial_rows = len(df)
            df = df.dropna()
            logger.info(f"Dropped {initial_rows - len(df)} rows with missing values")
        elif handle_missing == "fill":
            df = df.fillna(df.mean(numeric_only=True))
            logger.info("Filled missing values with column means")

        return df

    def encode_categorical(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = "label"
    ) -> pd.DataFrame:
        """
        Encode categorical variables.

        Args:
            df: Input DataFrame
            columns: Columns to encode (None = auto-detect)
            method: Encoding method ('label', 'onehot')

        Returns:
            DataFrame with encoded categories
        """
        logger.info(f"Encoding categorical variables using {method} encoding")

        df = df.copy()

        if columns is None:
            columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

        if method == "label":
            from sklearn.preprocessing import LabelEncoder
            for col in columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
        elif method == "onehot":
            df = pd.get_dummies(df, columns=columns, drop_first=True)

        return df

    def scale_features(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = "standard"
    ) -> pd.DataFrame:
        """
        Scale numerical features.

        Args:
            df: Input DataFrame
            columns: Columns to scale (None = all numeric)
            method: Scaling method ('standard', 'minmax', 'robust')

        Returns:
            DataFrame with scaled features
        """
        logger.info(f"Scaling features using {method} scaling")

        df = df.copy()

        if columns is None:
            columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if method == "standard":
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
        elif method == "minmax":
            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()
        elif method == "robust":
            from sklearn.preprocessing import RobustScaler
            scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")

        df[columns] = scaler.fit_transform(df[columns])

        return df

    def split_data(
        self,
        df: pd.DataFrame,
        target_column: str,
        test_size: float = 0.2,
        random_state: int = 42,
        stratify: bool = True
    ) -> tuple:
        """
        Split data into train and test sets.

        Args:
            df: Input DataFrame
            target_column: Name of target column
            test_size: Proportion of data for test set
            random_state: Random seed
            stratify: Whether to stratify split by target

        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        logger.info(f"Splitting data: {1-test_size:.0%} train, {test_size:.0%} test")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        stratify_param = y if stratify else None

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify_param
        )

        logger.info(f"Train set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")

        return X_train, X_test, y_train, y_test
