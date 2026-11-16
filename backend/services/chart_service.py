
def recommend_chart(df):

    if df.empty:
        return {
            "chart_type": "none",
            "reason": "No data available to visualize."
        }

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    category_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if not numeric_columns:
        return {
            "chart_type": "none",
            "reason": "No numerical columns available."
        }

    if not category_columns:
        return {
            "chart_type": "bar",
            "reason": "Numerical data can be compared."
        }

    category = category_columns[0]
    metric = numeric_columns[0]

    # Time-based data is better displayed as a line chart
    if any(
        word in category.lower()
        for word in ["year", "date", "month", "time"]
    ):
        chart_type = "line"
        reason = "Line charts help identify trends over time."

    # Small category sets can be displayed as pie charts
    elif df[category].nunique() <= 5:
        chart_type = "pie"
        reason = "Pie charts help compare proportions."

    else:
        chart_type = "bar"
        reason = "Bar charts help compare categories."

    return {
        "chart_type": chart_type,
        "category": category,
        "metric": metric,
        "reason": reason
    }
