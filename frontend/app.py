
import streamlit as st
import requests
import pandas as pd
import sys
import plotly.express as px
from pathlib import Path

SERVICES_DIR = Path(__file__).resolve().parents[1] / "backend" / "services"
sys.path.insert(0, str(SERVICES_DIR))

from chart_service import recommend_chart
from comparison_service import compare_datasets

API_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: white;
}
h1, h2, h3 {
    color: #60a5fa;
}
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
}
.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

if "dataset_uploaded" not in st.session_state:
    st.session_state.dataset_uploaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# HEADER
st.title("📊 InsightIQ")
st.subheader("AI-Powered Data Analytics Assistant")
st.write("Transform your datasets into meaningful insights using Artificial Intelligence.")

st.divider()

# DATASET UPLOAD
st.header("📁 Upload Your Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    key="main_dataset"
)

if uploaded_file is not None:

    if st.button("Upload Dataset"):

        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            with st.spinner("Uploading your dataset..."):
                response = requests.post(
                    f"{API_URL}/api/upload",
                    files=files,
                    timeout=60
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.dataset_uploaded = True
                st.session_state.chat_history = []
                st.session_state.analysis_result = None

                st.success("Dataset uploaded successfully!")

                profile = data["profile"]

                col1, col2 = st.columns(2)
                col1.metric("Total Rows", profile["total_rows"])
                col2.metric("Total Columns", profile["total_columns"])

                st.subheader("📋 Dataset Information")
                st.write(", ".join(profile["columns"]))

                st.subheader("Dataset Preview")
                st.dataframe(
                    pd.DataFrame(profile["preview"]),
                    use_container_width=True
                )

                st.subheader("Missing Values")

                missing_df = pd.DataFrame(
                    list(profile["missing_values"].items()),
                    columns=["Column", "Missing Values"]
                )

                st.dataframe(missing_df, use_container_width=True)

            else:
                st.error(response.text)

        except requests.exceptions.RequestException as error:
            st.error(f"Backend connection error: {error}")

st.divider()

# ASK INSIGHTIQ
st.header("🤖 Ask InsightIQ")

question = st.text_input(
    "Ask anything about your dataset",
    placeholder="Example: Show the top 10 directors by total votes"
)

if st.button("🚀 Analyze"):

    if not question.strip():
        st.warning("Please enter a question.")

    elif not st.session_state.dataset_uploaded:
        st.warning("Please upload a dataset first.")

    else:

        try:
            with st.spinner("InsightIQ is analyzing your data..."):

                response = requests.post(
                    f"{API_URL}/api/ask",
                    json={"question": question},
                    timeout=180
                )

            if response.status_code == 200:

                result = response.json()

                st.session_state.analysis_result = result

                st.session_state.chat_history.append({
                    "question": question,
                    "answer": result["answer"]
                })

            else:
                st.error(response.text)

        except requests.exceptions.RequestException as error:
            st.error(f"Backend connection error: {error}")

# DISPLAY RESULTS
result = st.session_state.analysis_result

if result is not None:

    st.success("Analysis completed successfully!")

    st.subheader("💡 AI Insight")
    st.markdown(result["answer"])

    st.subheader("📝 Generated SQL")
    st.code(result["sql"], language="sql")

    result_df = pd.DataFrame(result["result"])

    st.subheader("📊 Query Results")
    st.dataframe(result_df, use_container_width=True)

    if not result_df.empty:

        csv_data = result_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Results as CSV",
            data=csv_data,
            file_name="insightiq_results.csv",
            mime="text/csv"
        )

        # INTERACTIVE CHARTS
        st.divider()
        st.subheader("📈 Interactive Data Visualization")

        recommendation = recommend_chart(result_df)

        st.info(
            f"Recommended: {recommendation['chart_type'].upper()} chart — "
            f"{recommendation['reason']}"
        )

        if "category" in recommendation:

            category = recommendation["category"]
            metric = recommendation["metric"]

            chart_df = (
                result_df
                .groupby(category, as_index=False)[metric]
                .sum()
                .sort_values(metric, ascending=False)
            )

            chart_type = recommendation["chart_type"]

            if chart_type == "bar":
                fig = px.bar(
                    chart_df,
                    x=category,
                    y=metric,
                    title=f"{metric} by {category}",
                    text_auto=True
                )

            elif chart_type == "line":
                fig = px.line(
                    chart_df,
                    x=category,
                    y=metric,
                    title=f"{metric} Trend",
                    markers=True
                )

            elif chart_type == "pie":
                fig = px.pie(
                    chart_df,
                    names=category,
                    values=metric,
                    title=f"{metric} Distribution",
                    hole=0.4
                )

            else:
                fig = None

            if fig is not None:
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#0b1120",
                    plot_bgcolor="#0b1120",
                    font_color="white"
                )

                st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("This result does not have a category column for comparison.")

# DATASET COMPARISON
st.divider()
st.header("⚖️ Dataset Comparison")

st.write("Upload two CSV datasets to compare their structure and numerical metrics.")

col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader(
        "Upload First Dataset",
        type=["csv"],
        key="compare_file_1"
    )

with col2:
    file2 = st.file_uploader(
        "Upload Second Dataset",
        type=["csv"],
        key="compare_file_2"
    )

if st.button("🔍 Compare Datasets"):

    if file1 is None or file2 is None:
        st.warning("Please upload both CSV datasets.")

    else:
        try:
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)

            comparison = compare_datasets(df1, df2)

            st.success("Dataset comparison completed!")

            metric1, metric2 = st.columns(2)

            metric1.metric(
                "First Dataset Rows",
                comparison["dataset_1_rows"]
            )

            metric2.metric(
                "Second Dataset Rows",
                comparison["dataset_2_rows"]
            )

            st.subheader("Common Columns")
            st.write(comparison["common_columns"] or "No common columns")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Unique to First Dataset")
                st.write(comparison["unique_to_dataset_1"] or "None")

            with col2:
                st.write("Unique to Second Dataset")
                st.write(comparison["unique_to_dataset_2"] or "None")

            st.subheader("Numerical Metric Comparison")

            metric_data = comparison["metric_comparison"]

            if metric_data:

                metric_df = pd.DataFrame.from_dict(
                    metric_data,
                    orient="index"
                ).reset_index()

                metric_df.rename(
                    columns={"index": "Metric"},
                    inplace=True
                )

                st.dataframe(
                    metric_df,
                    use_container_width=True
                )

                st.subheader("📊 Comparison Chart")

                chart_df = metric_df.melt(
                    id_vars="Metric",
                    value_vars=[
                        "dataset_1_total",
                        "dataset_2_total"
                    ],
                    var_name="Dataset",
                    value_name="Total"
                )

                fig = px.bar(
                    chart_df,
                    x="Metric",
                    y="Total",
                    color="Dataset",
                    barmode="group",
                    title="Numerical Metrics Comparison"
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#0b1120",
                    plot_bgcolor="#0b1120",
                    font_color="white"
                )

                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("No common numerical columns found.")

        except Exception as error:
            st.error(f"Comparison failed: {error}")

# CHAT HISTORY
st.divider()
st.header("💬 Previous Questions")

if st.session_state.chat_history:

    for index, chat in enumerate(
        reversed(st.session_state.chat_history),
        start=1
    ):

        with st.expander(f"Question {index}: {chat['question']}"):
            st.write(chat["answer"])

else:
    st.info("Your previous questions will appear here.")

st.divider()

st.caption("InsightIQ | AI-Powered Data Analytics Assistant")
