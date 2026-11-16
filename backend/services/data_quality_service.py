
import pandas as pd


def analyze_data_quality(df):

    if df.empty:
        raise ValueError("Dataset is empty.")

    total_rows = len(df)
    total_columns = len(df.columns)

    # Missing values
    missing_values = df.isnull().sum()

    total_missing = int(missing_values.sum())

    missing_details = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    # Duplicate records
    duplicate_count = int(df.duplicated().sum())

    # Numerical statistics
    numeric_df = df.select_dtypes(include="number")

    numerical_statistics = {}

    for column in numeric_df.columns:

        numerical_statistics[column] = {
            "mean": round(float(numeric_df[column].mean()), 2),
            "median": round(float(numeric_df[column].median()), 2),
            "minimum": round(float(numeric_df[column].min()), 2),
            "maximum": round(float(numeric_df[column].max()), 2)
        }

    # Dataset quality score
    total_cells = total_rows * total_columns

    missing_percentage = (
        total_missing / total_cells * 100
    )

    duplicate_percentage = (
        duplicate_count / total_rows * 100
    )

    quality_score = max(
        0,
        round(100 - missing_percentage - duplicate_percentage, 2)
    )

    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "missing_values": missing_details,
        "total_missing_values": total_missing,
        "duplicate_records": duplicate_count,
        "numerical_statistics": numerical_statistics,
        "quality_score": quality_score
    }
