# InsightIQ – AI-Powered Data Analytics Assistant

## Overview

InsightIQ is an AI-powered data analytics application that allows users to upload CSV datasets and interact with their data using natural language.

It uses Google Gemini to convert user questions into SQL queries, DuckDB to execute them, and LangGraph to coordinate the analytics workflow. The application generates meaningful insights and visualizations without requiring users to write SQL manually.

## Key Features

- **CSV Data Upload:** Upload and analyze custom CSV datasets.
- **Natural Language Querying:** Ask questions about your data using simple English.
- **AI SQL Generation:** Generate DuckDB-compatible SQL queries using Google Gemini.
- **SQL Validation:** Validate generated queries before execution.
- **Automated Query Execution:** Execute queries using DuckDB.
- **AI-Generated Insights:** Convert query results into understandable explanations.
- **Automatic Chart Recommendations:** Generate visualizations based on query results.
- **Dataset Comparison:** Compare two datasets and analyze common columns and numerical metrics.
- **Data Quality Analysis:** Identify missing values, duplicate records and numerical statistics.
- **AI Data Cleaning Recommendations:** Receive suggestions for improving dataset quality.
- **SQL Error Recovery:** Attempt automatic correction when query execution fails.
- **Interactive Dashboard:** Explore results through a Streamlit interface.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | Flask |
| AI Model | Google Gemini |
| Workflow Orchestration | LangGraph |
| Database | DuckDB |
| Data Processing | Pandas |
| Visualization | Plotly |
| API Communication | REST API |

## System Architecture

```text
             USER
               |
               v
       STREAMLIT FRONTEND
               |
               v
          FLASK API
               |
               v
       LANGGRAPH WORKFLOW
               |
               v
       GEMINI SQL GENERATION
               |
               v
          SQL VALIDATION
               |
               v
        DUCKDB EXECUTION
               |
               v
       AI INSIGHT GENERATION
               |
               v
       RESULTS & VISUALIZATION
```

## Project Structure

```text
Insight IQ/
│
├── backend/
│   ├── routes/
│   ├── services/
│   ├── graph/
│   └── app.py
│
├── frontend/
│   ├── app.py
│   └── pages/
│       └── 2_Data_Quality.py
│
├── data/
├── config/
├── tests/
├── requirements.txt
├── .env
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "Insight IQ"
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Use your own Gemini API key. Never upload your actual API key to GitHub.

### 5. Start the Backend

Open a terminal and run:

```bash
python backend/app.py
```

### 6. Start the Frontend

Open another terminal and run:

```bash
streamlit run frontend/app.py
```

Open the local application at:

```text
http://localhost:8501
```

## How It Works

1. The user uploads a CSV dataset.
2. The backend processes and stores the dataset in DuckDB.
3. The user enters a question in natural language.
4. Gemini generates an SQL query based on the dataset schema.
5. The query is validated.
6. DuckDB executes the query.
7. LangGraph coordinates the workflow.
8. Gemini generates a natural-language explanation.
9. Streamlit displays the results and recommended visualizations.

## Future Improvements

- Automated data cleaning and export.
- Enhanced query security and performance optimization.
- Support for additional file formats.
- Improved dashboard customization.
- Cloud deployment and scalability.

## Project Goal

The goal of InsightIQ is to make data analytics more accessible by combining artificial intelligence, natural language processing, database querying and interactive visualization in one application.

---

**InsightIQ – Ask Questions. Discover Insights. Make Better Decisions.**