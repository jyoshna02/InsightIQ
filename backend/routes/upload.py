
from flask import Blueprint, request, jsonify
import traceback
import sys
from pathlib import Path

from services.data_loader import load_dataset, profile_dataset
from services.duckdb_service import store_dataset


upload_bp = Blueprint("upload", __name__)


# --------------------------------
# API 1: Upload CSV Dataset
# --------------------------------

@upload_bp.route("/api/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["file"]

    if not file.filename.lower().endswith(".csv"):
        return jsonify({
            "error": "Please upload a CSV file"
        }), 400

    try:
        df = load_dataset(file)

        if df.empty:
            return jsonify({
                "error": "The uploaded CSV is empty"
            }), 400

        total_rows = store_dataset(df)
        profile = profile_dataset(df)

        return jsonify({
            "message": "Dataset uploaded successfully!",
            "database_rows": total_rows,
            "profile": profile
        }), 200

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "error": str(error)
        }), 500


# --------------------------------
# API 2: Ask AI Analytics Question
# --------------------------------

@upload_bp.route("/api/ask", methods=["POST"])
def ask_question():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "question" not in data:
        return jsonify({
            "error": "Please provide a question"
        }), 400

    question = data["question"]

    if not isinstance(question, str) or not question.strip():
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    try:
        backend_dir = Path(__file__).resolve().parents[1]
        graph_dir = backend_dir / "graph"

        if str(graph_dir) not in sys.path:
            sys.path.insert(0, str(graph_dir))

        from analytics_graph import analytics_graph

        result = analytics_graph.invoke({
            "question": question.strip()
        })

        return jsonify({
            "question": result["question"],
            "sql": result["sql_query"],
            "result": result["query_result"],
            "answer": result["answer"]
        }), 200

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "error": str(error)
        }), 500
