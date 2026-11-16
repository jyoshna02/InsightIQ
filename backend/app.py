
from flask import Flask, jsonify
from routes.upload import upload_bp

app = Flask(__name__)

# Register upload and question APIs
app.register_blueprint(upload_bp)

@app.route("/")
def home():
    return jsonify({
        "project": "InsightIQ",
        "message": "AI Analytics Backend is Running!",
        "status": "Success"
    })

@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy"
    })

if __name__ == "__main__":
    print("\n========== REGISTERED ROUTES ==========")
    print(app.url_map)
    app.run(debug=True, port=5000)
