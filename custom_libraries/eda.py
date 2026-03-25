"""
Simple EDA Utility Module
A comprehensive toolkit for exploratory data analysis of DataFrames and CSV files.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


# ============================================================================
# DATA LOADING
# ============================================================================

def load_data(path: str, **kwargs) -> pd.DataFrame:
    """
    Load data from various file formats.
    
    Args:
        path: File path to load
        **kwargs: Additional arguments for pandas read functions
        
    Returns:
        Loaded DataFrame
    """
    file_type = path.split('.')[-1].lower()
    
    loaders = {
        'csv': pd.read_csv,
        'xlsx': pd.read_excel,
        'xls': pd.read_excel,
        'json': pd.read_json,
        'parquet': pd.read_parquet,
        'pickle': pd.read_pickle,
        'pkl': pd.read_pickle,
    }
    
    if file_type not in loaders:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    print(f"Loading data from {path}...")
    data = loaders[file_type](path, **kwargs)
    print(f"✓ Loaded {len(data)} rows and {len(data.columns)} columns")
    
    return data


# ============================================================================
# BASIC SUMMARY FUNCTIONS
# ============================================================================

def quick_summary(df: pd.DataFrame) -> None:
    """
    Display a quick summary of the DataFrame.
    
    Args:
        df: Input DataFrame
    """
    print("=" * 80)
    print("QUICK SUMMARY")
    print("=" * 80)
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Duplicate Rows: {df.duplicated().sum()}")
    print("\n")


def data_info(df: pd.DataFrame) -> None:
    """
    Display detailed information about the DataFrame.
    
    Args:
        df: Input DataFrame
    """
    print("=" * 80)
    print("DATA INFO")
    print("=" * 80)
    print(df.info())
    print("\n")


def data_description(df: pd.DataFrame) -> None:
    """
    Display statistical description of numerical columns.
    
    Args:
        df: Input DataFrame
    """
    print("=" * 80)
    print("STATISTICAL DESCRIPTION")
    print("=" * 80)
    print(df.describe())
    print("\n")
    
    # Also describe categorical columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        print("=" * 80)
        print("CATEGORICAL COLUMNS DESCRIPTION")
        print("=" * 80)
        print(df[categorical_cols].describe())
        print("\n")


def missing_data_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing data in the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with missing data statistics
    """
    print("=" * 80)
    print("MISSING DATA SUMMARY")
    print("=" * 80)
    
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100
    empty_string_count = (df == '').sum()
    
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_count.values,
        'Missing_Percent': missing_percent.values,
        'Empty_Strings': empty_string_count.values,
        'Data_Type': df.dtypes.values
    })
    
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values(
        'Missing_Percent', ascending=False
    )
    
    if len(missing_df) > 0:
        print(missing_df.to_string(index=False))
    else:
        print("✓ No missing values found!")
    
    print("\n")
    return missing_df


def duplicate_analysis(df: pd.DataFrame) -> None:
    """
    Analyze duplicate rows in the DataFrame.
    
    Args:
        df: Input DataFrame
    """
    print("=" * 80)
    print("DUPLICATE ANALYSIS")
    print("=" * 80)
    
    total_duplicates = df.duplicated().sum()
    duplicate_percent = (total_duplicates / len(df)) * 100
    
    print(f"Total Duplicates: {total_duplicates} ({duplicate_percent:.2f}%)")
    
    if total_duplicates > 0:
        print("\nSample duplicate rows:")
        print(df[df.duplicated()].head())
    
    print("\n")


def data_types_summary(df: pd.DataFrame) -> None:
    """
    Summarize data types in the DataFrame.
    
    Args:
        df: Input DataFrame
    """
    print("=" * 80)
    print("DATA TYPES SUMMARY")
    print("=" * 80)
    
    dtype_counts = df.dtypes.value_counts()
    print(dtype_counts)
    
    print("\nColumns by data type:")
    for dtype in dtype_counts.index:
        cols = df.select_dtypes(include=[dtype]).columns.tolist()
        print(f"\n{dtype}: {len(cols)} columns")
        print(f"  {', '.join(cols[:10])}" + ("..." if len(cols) > 10 else ""))
    
    print("\n")


# ============================================================================
# COMPLETE SUMMARY
# ============================================================================

def full_summary(df: pd.DataFrame) -> None:
    """
    Generate a comprehensive summary of the DataFrame.
    
    Args:
        df: Input DataFrame
    """
    quick_summary(df)
    data_info(df)
    data_description(df)
    data_types_summary(df)
    missing_data_summary(df)
    duplicate_analysis(df)


# ============================================================================
# COLUMN ANALYSIS
# ============================================================================

def column_summary(df: pd.DataFrame, column: str, show_plots: bool = True) -> None:
    """
    Detailed analysis of a single column.
    
    Args:
        df: Input DataFrame
        column: Column name to analyze
        show_plots: Whether to display plots
    """
    if column not in df.columns:
        print(f"Error: Column '{column}' not found in DataFrame")
        return
    
    print("=" * 80)
    print(f"COLUMN ANALYSIS: {column}")
    print("=" * 80)
    
    col_data = df[column]
    
    # Basic info
    print(f"Data Type: {col_data.dtype}")
    print(f"Total Values: {len(col_data)}")
    print(f"Unique Values: {col_data.nunique()}")
    print(f"Missing Values: {col_data.isnull().sum()} ({(col_data.isnull().sum()/len(col_data)*100):.2f}%)")
    
    if col_data.dtype == 'object':
        print(f"Empty Strings: {(col_data == '').sum()}")
    
    print("\n")
    
    # Statistical summary
    if pd.api.types.is_numeric_dtype(col_data):
        print("Statistical Summary:")
        print("-" * 80)
        print(col_data.describe())
        print("\n")
    
    # Value counts
    print("Top 20 Value Counts:")
    print("-" * 80)
    value_counts = col_data.value_counts().head(20)
    print(value_counts)
    print("\n")
    
    # Plots
    if show_plots:
        _plot_column(df, column)


def _plot_column(df: pd.DataFrame, column: str) -> None:
    """
    Create visualizations for a column.
    
    Args:
        df: Input DataFrame
        column: Column name to plot
    """
    col_data = df[column].dropna()
    
    if pd.api.types.is_numeric_dtype(col_data):
        # Numeric column plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Analysis of {column}', fontsize=16, fontweight='bold')
        
        # Histogram
        axes[0, 0].hist(col_data, bins=30, edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Histogram')
        axes[0, 0].set_xlabel(column)
        axes[0, 0].set_ylabel('Frequency')
        
        # Box plot
        axes[0, 1].boxplot(col_data, vert=True)
        axes[0, 1].set_title('Box Plot')
        axes[0, 1].set_ylabel(column)
        
        # KDE plot
        col_data.plot(kind='density', ax=axes[1, 0])
        axes[1, 0].set_title('Density Plot')
        axes[1, 0].set_xlabel(column)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(col_data, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot')
        
        plt.tight_layout()
        plt.show()
        
    else:
        # Categorical column plots
        value_counts = col_data.value_counts().head(20)
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle(f'Analysis of {column}', fontsize=16, fontweight='bold')
        
        # Bar plot
        value_counts.plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
        axes[0].set_title('Value Counts (Top 20)')
        axes[0].set_xlabel(column)
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Pie chart (top 10)
        top_10 = value_counts.head(10)
        axes[1].pie(top_10, labels=top_10.index, autopct='%1.1f%%', startangle=90)
        axes[1].set_title('Distribution (Top 10)')
        
        plt.tight_layout()
        plt.show()


def compare_columns(df: pd.DataFrame, col1: str, col2: str) -> None:
    """
    Compare two columns and their relationship.
    
    Args:
        df: Input DataFrame
        col1: First column name
        col2: Second column name
    """
    print("=" * 80)
    print(f"COMPARING: {col1} vs {col2}")
    print("=" * 80)
    
    # Check if both are numeric
    if pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2]):
        correlation = df[[col1, col2]].corr().iloc[0, 1]
        print(f"Correlation: {correlation:.4f}")
        print("\n")
        
        # Scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(df[col1], df[col2], alpha=0.5)
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title(f'{col1} vs {col2} (Correlation: {correlation:.4f})')
        plt.grid(True, alpha=0.3)
        plt.show()
        
    else:
        # Cross-tabulation for categorical
        crosstab = pd.crosstab(df[col1], df[col2])
        print("Cross-tabulation:")
        print(crosstab)
        print("\n")
        
        # Heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(crosstab, annot=True, fmt='d', cmap='YlOrRd')
        plt.title(f'{col1} vs {col2}')
        plt.tight_layout()
        plt.show()


# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

def correlation_analysis(df: pd.DataFrame, method: str = 'pearson') -> None:
    """
    Analyze correlations between numeric columns.
    
    Args:
        df: Input DataFrame
        method: Correlation method ('pearson', 'spearman', 'kendall')
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        print("Not enough numeric columns for correlation analysis")
        return
    
    print("=" * 80)
    print(f"CORRELATION ANALYSIS ({method.upper()})")
    print("=" * 80)
    
    corr_matrix = df[numeric_cols].corr(method=method)
    
    # Print high correlations
    print("\nHigh Correlations (|r| > 0.7):")
    print("-" * 80)
    
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > 0.7:
                high_corr.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j]
                ))
    
    if high_corr:
        for col1, col2, corr in sorted(high_corr, key=lambda x: abs(x[2]), reverse=True):
            print(f"{col1:20s} <-> {col2:20s}: {corr:6.3f}")
    else:
        print("No high correlations found")
    
    print("\n")
    
    # Correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title(f'Correlation Matrix ({method.capitalize()})')
    plt.tight_layout()
    plt.show()


# ============================================================================
# OUTLIER DETECTION
# ============================================================================

def detect_outliers(df: pd.DataFrame, method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
    """
    Detect outliers in numeric columns.
    
    Args:
        df: Input DataFrame
        method: Detection method ('iqr' or 'zscore')
        threshold: Threshold for outlier detection (1.5 for IQR, 3 for Z-score)
        
    Returns:
        DataFrame with outlier statistics
    """
    print("=" * 80)
    print(f"OUTLIER DETECTION ({method.upper()})")
    print("=" * 80)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_summary = []
    
    for col in numeric_cols:
        col_data = df[col].dropna()
        
        if method == 'iqr':
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = ((col_data < lower_bound) | (col_data > upper_bound)).sum()
            
        elif method == 'zscore':
            z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
            outliers = (z_scores > threshold).sum()
            lower_bound = col_data.mean() - threshold * col_data.std()
            upper_bound = col_data.mean() + threshold * col_data.std()
        
        outlier_summary.append({
            'Column': col,
            'Outliers': outliers,
            'Outlier_Percent': (outliers / len(col_data)) * 100,
            'Lower_Bound': lower_bound,
            'Upper_Bound': upper_bound
        })
    
    outlier_df = pd.DataFrame(outlier_summary)
    outlier_df = outlier_df[outlier_df['Outliers'] > 0].sort_values('Outliers', ascending=False)
    
    if len(outlier_df) > 0:
        print(outlier_df.to_string(index=False))
    else:
        print("✓ No outliers detected!")
    
    print("\n")
    return outlier_df


# ============================================================================
# DISTRIBUTION ANALYSIS
# ============================================================================

def distribution_analysis(df: pd.DataFrame) -> None:
    """
    Analyze distributions of numeric columns.
    
    Args:
        df: Input DataFrame
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        print("No numeric columns found")
        return
    
    print("=" * 80)
    print("DISTRIBUTION ANALYSIS")
    print("=" * 80)
    
    from scipy import stats
    
    dist_summary = []
    
    for col in numeric_cols:
        col_data = df[col].dropna()
        
        # Skewness and Kurtosis
        skewness = stats.skew(col_data)
        kurtosis = stats.kurtosis(col_data)
        
        # Normality test (Shapiro-Wilk for small samples)
        if len(col_data) < 5000:
            _, p_value = stats.shapiro(col_data)
        else:
            _, p_value = stats.normaltest(col_data)
        
        dist_summary.append({
            'Column': col,
            'Skewness': skewness,
            'Kurtosis': kurtosis,
            'Normality_pvalue': p_value,
            'Is_Normal': 'Yes' if p_value > 0.05 else 'No'
        })
    
    dist_df = pd.DataFrame(dist_summary)
    print(dist_df.to_string(index=False))
    print("\n")
    
    # Plot distributions
    n_cols = len(numeric_cols)
    n_rows = (n_cols + 2) // 3
    
    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]
    
    for idx, col in enumerate(numeric_cols):
        df[col].hist(bins=30, ax=axes[idx], edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'{col}\nSkew: {dist_df.iloc[idx]["Skewness"]:.2f}')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Frequency')
    
    # Hide empty subplots
    for idx in range(n_cols, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()


# ============================================================================
# CATEGORICAL ANALYSIS
# ============================================================================

def categorical_analysis(df: pd.DataFrame, top_n: int = 10) -> None:
    """
    Analyze categorical columns in the DataFrame.
    
    Args:
        df: Input DataFrame
        top_n: Number of top categories to display
    """
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    if len(categorical_cols) == 0:
        print("No categorical columns found")
        return
    
    print("=" * 80)
    print("CATEGORICAL ANALYSIS")
    print("=" * 80)
    
    for col in categorical_cols:
        print(f"\n{col}:")
        print("-" * 80)
        
        value_counts = df[col].value_counts()
        print(f"Unique Values: {len(value_counts)}")
        print(f"Most Common: {value_counts.index[0]} ({value_counts.iloc[0]} occurrences)")
        
        print(f"\nTop {top_n} Values:")
        print(value_counts.head(top_n))
        print("\n")


# ============================================================================
# TIME SERIES ANALYSIS
# ============================================================================

def time_series_analysis(df: pd.DataFrame, date_column: str, value_column: str) -> None:
    """
    Analyze time series data.
    
    Args:
        df: Input DataFrame
        date_column: Name of date column
        value_column: Name of value column to analyze
    """
    print("=" * 80)
    print(f"TIME SERIES ANALYSIS: {value_column} over {date_column}")
    print("=" * 80)
    
    df_ts = df.copy()
    df_ts[date_column] = pd.to_datetime(df_ts[date_column])
    df_ts = df_ts.sort_values(date_column)
    
    # Basic statistics
    print(f"Date Range: {df_ts[date_column].min()} to {df_ts[date_column].max()}")
    print(f"Total Period: {(df_ts[date_column].max() - df_ts[date_column].min()).days} days")
    print(f"Number of Records: {len(df_ts)}")
    print("\n")
    
    # Plot
    plt.figure(figsize=(15, 6))
    plt.plot(df_ts[date_column], df_ts[value_column], linewidth=1)
    plt.xlabel(date_column)
    plt.ylabel(value_column)
    plt.title(f'{value_column} over Time')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ============================================================================
# GROUP ANALYSIS
# ============================================================================

def group_analysis(df: pd.DataFrame, group_cols: Union[str, List[str]], 
                   agg_col: str = None, agg_func: str = 'mean') -> pd.DataFrame:
    """
    Analyze data by groups.
    
    Args:
        df: Input DataFrame
        group_cols: Column(s) to group by
        agg_col: Column to aggregate (None for count)
        agg_func: Aggregation function ('mean', 'sum', 'count', 'median', etc.)
        
    Returns:
        Grouped DataFrame
    """
    if isinstance(group_cols, str):
        group_cols = [group_cols]
    
    print("=" * 80)
    print(f"GROUP ANALYSIS: By {', '.join(group_cols)}")
    print("=" * 80)
    
    if agg_col is None:
        result = df.groupby(group_cols).size().reset_index(name='count')
        result = result.sort_values('count', ascending=False)
    else:
        result = df.groupby(group_cols)[agg_col].agg(agg_func).reset_index()
        result = result.sort_values(agg_col, ascending=False)
    
    print(result.head(20))
    print("\n")
    
    return result


# ============================================================================
# EXPORT REPORT
# ============================================================================

def export_report(df: pd.DataFrame, output_path: str = 'eda_report.html') -> None:
    """
    Export a comprehensive HTML report of the DataFrame.
    
    Args:
        df: Input DataFrame
        output_path: Path to save the HTML report
    """
    try:
        import pandas_profiling
        profile = pandas_profiling.ProfileReport(df, title="EDA Report", explorative=True)
        profile.to_file(output_path)
        print(f"✓ Report exported to {output_path}")
    except ImportError:
        print("pandas_profiling not installed. Install with: pip install pandas-profiling")


# ============================================================================
# MAIN EDA FUNCTION
# ============================================================================

def eda(df: pd.DataFrame, detailed: bool = True, plots: bool = True) -> None:
    """
    Perform complete exploratory data analysis.
    
    Args:
        df: Input DataFrame
        detailed: Whether to show detailed analysis
        plots: Whether to show plots
    """
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "EXPLORATORY DATA ANALYSIS" + " " * 33 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    # Basic summary
    full_summary(df)
    
    if detailed:
        # Distribution analysis
        distribution_analysis(df)
        
        # Correlation analysis
        if len(df.select_dtypes(include=[np.number]).columns) >= 2:
            correlation_analysis(df)
        
        # Outlier detection
        detect_outliers(df)
        
        # Categorical analysis
        categorical_analysis(df)
    
    print("=" * 80)
    print("EDA COMPLETE!")
    print("=" * 80)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example usage
    # df = load_data('your_data.csv')
    # eda(df)
    # column_summary(df, 'column_name')
    # correlation_analysis(df)
    pass
