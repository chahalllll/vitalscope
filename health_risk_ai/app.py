from flask import Flask, jsonify, render_template, request
from engine import assess, METRICS, FEATURES, DISEASES

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/assess")
def api_assess():
    try:
        return jsonify(assess(request.get_json(force=True) or {}))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.get("/api/metrics")
def api_metrics():
    return jsonify(METRICS)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
