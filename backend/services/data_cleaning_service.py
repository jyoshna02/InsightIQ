
import pandas as pd


def recommend_cleaning(df):

    if df.empty:
        raise ValueError("Dataset is empty.")

    recommendations = []

    # 1. Check missing values
    for column in df.columns:

        missing_count = int(df[column].isnull().sum())

        if missing_count > 0:

            if pd.api.types.is_numeric_dtype(df[column]):
                method = "Consider filling missing values with the median."

            else:
                method = "Consider filling missing values with the mode or 'Unknown'."

            recommendations.append({
                "column": column,
                "issue": "Missing Values",
                "count": missing_count,
                "recommendation": method
            })

    # 2. Check duplicate records
    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:

        recommendations.append({
            "column": "All Columns",
            "issue": "Duplicate Records",
            "count": duplicate_count,
            "recommendation": "Review duplicate rows before removing them."
        })

    # 3. Check possible incorrect numerical data types
    for column in df.select_dtypes(include="object").columns:

        converted = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        original_non_null = df[column].notna().sum()

        if original_non_null > 0:

            convertible_count = converted.notna().sum()

            if convertible_count == original_non_null:

                recommendations.append({
                    "column": column,
                    "issue": "Possible Data Type Issue",
                    "count": int(original_non_null),
                    "recommendation": "This column contains numeric values stored as text. Consider converting it to a numeric type."
                })

    # 4. Final report
    return {
        "total_issues": len(recommendations),
        "recommendations": recommendations,
        "status": (
            "Cleaning recommendations generated."
            if recommendations
            else "No common data quality issues detected."
        )
    }
