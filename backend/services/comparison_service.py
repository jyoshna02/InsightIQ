
import pandas as pd


def compare_datasets(df1, df2):

    if df1.empty or df2.empty:
        raise ValueError("Both datasets must contain data.")

    common_columns = list(
        set(df1.columns) & set(df2.columns)
    )

    unique_to_first = list(
        set(df1.columns) - set(df2.columns)
    )

    unique_to_second = list(
        set(df2.columns) - set(df1.columns)
    )

    numeric_columns = [
        col for col in common_columns
        if pd.api.types.is_numeric_dtype(df1[col])
        and pd.api.types.is_numeric_dtype(df2[col])
    ]

    metric_comparison = {}

    for column in numeric_columns:

        metric_comparison[column] = {
            "dataset_1_total": float(df1[column].sum()),
            "dataset_2_total": float(df2[column].sum()),
            "difference": float(
                df2[column].sum() - df1[column].sum()
            )
        }

    return {
        "dataset_1_rows": len(df1),
        "dataset_2_rows": len(df2),
        "common_columns": common_columns,
        "unique_to_dataset_1": unique_to_first,
        "unique_to_dataset_2": unique_to_second,
        "metric_comparison": metric_comparison
    }
