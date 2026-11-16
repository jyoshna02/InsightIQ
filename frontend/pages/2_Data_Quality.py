
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

SERVICES_DIR = (
    Path(__file__).resolve().parents[2]
    / "backend"
    / "services"
)

sys.path.insert(0, str(SERVICES_DIR))

from data_quality_service import analyze_data_quality
from data_cleaning_service import recommend_cleaning

st.set_page_config(
    page_title="InsightIQ - Data Quality",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Data Quality Analyzer")
st.subheader("Discover and improve your dataset quality")

st.write(
    "Analyze missing values, duplicate records, "
    "numerical statistics and recommended cleaning actions."
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        st.success("Dataset loaded successfully!")

        # DATASET OVERVIEW
        st.subheader("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", len(df))
        col2.metric("Total Columns", len(df.columns))
        col3.metric("Duplicate Rows", int(df.duplicated().sum()))

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        # QUALITY REPORT
        report = analyze_data_quality(df)

        st.divider()
        st.subheader("⭐ Dataset Quality Score")

        score = report["quality_score"]

        st.metric("Quality Score", f"{score}%")
        st.progress(score / 100)

        if score >= 90:
            st.success("Excellent data quality!")

        elif score >= 70:
            st.warning("Good data quality. Some improvements are needed.")

        else:
            st.error("Poor data quality. Cleaning is recommended.")

        # MISSING VALUES
        st.divider()
        st.subheader("❗ Missing Values")

        if report["missing_values"]:

            missing_df = pd.DataFrame(
                list(report["missing_values"].items()),
                columns=["Column", "Missing Values"]
            )

            st.dataframe(
                missing_df,
                use_container_width=True
            )

        else:
            st.success("No missing values found!")

        st.metric(
            "Total Missing Values",
            report["total_missing_values"]
        )

        # DUPLICATES
        st.divider()
        st.subheader("🔁 Duplicate Records")

        st.metric(
            "Duplicate Rows",
            report["duplicate_records"]
        )

        if report["duplicate_records"] > 0:
            st.warning("Duplicate records detected.")

        else:
            st.success("No duplicate records found!")

        # NUMERICAL STATISTICS
        st.divider()
        st.subheader("📈 Numerical Statistics")

        if report["numerical_statistics"]:

            stats_df = pd.DataFrame.from_dict(
                report["numerical_statistics"],
                orient="index"
            )

            stats_df.index.name = "Column"

            st.dataframe(
                stats_df,
                use_container_width=True
            )

        else:
            st.info("No numerical columns found.")

        # AI CLEANING RECOMMENDATIONS
        st.divider()
        st.header("🤖 AI Data Cleaning Assistant")

        st.write(
            "InsightIQ identifies common data issues "
            "and recommends suitable cleaning methods."
        )

        cleaning_report = recommend_cleaning(df)

        st.metric(
            "Issues Detected",
            cleaning_report["total_issues"]
        )

        if cleaning_report["recommendations"]:

            cleaning_df = pd.DataFrame(
                cleaning_report["recommendations"]
            )

            st.dataframe(
                cleaning_df,
                use_container_width=True
            )

            st.info(
                "These are recommendations only. "
                "Your original dataset has not been modified."
            )

        else:
            st.success(cleaning_report["status"])

        # DOWNLOAD REPORT
        st.divider()
        st.subheader("📥 Download Quality Report")

        report_df = pd.DataFrame([
            {"Metric": "Total Rows", "Value": report["total_rows"]},
            {"Metric": "Total Columns", "Value": report["total_columns"]},
            {"Metric": "Missing Values", "Value": report["total_missing_values"]},
            {"Metric": "Duplicate Records", "Value": report["duplicate_records"]},
            {"Metric": "Quality Score", "Value": f"{score}%"},
            {"Metric": "Detected Cleaning Issues", "Value": cleaning_report["total_issues"]}
        ])

        st.download_button(
            "⬇️ Download Quality Report",
            data=report_df.to_csv(index=False).encode("utf-8"),
            file_name="insightiq_quality_report.csv",
            mime="text/csv"
        )

    except Exception as error:
        st.error(f"Analysis failed: {error}")

else:
    st.info("Upload a CSV file to start your data quality analysis.")

st.caption(
    "InsightIQ | Intelligent Data Quality & Cleaning Assistant"
)
