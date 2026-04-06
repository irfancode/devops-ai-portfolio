from flask import Flask, jsonify, request
import time
import os
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("http_request_duration_seconds", "HTTP request duration", ["endpoint"])

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "apidb")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route("/api/orders", methods=["GET"])
def get_orders():
    start = time.time()
    REQUEST_DURATION.labels(endpoint="/orders").observe(time.time() - start)
    REQUEST_COUNT.labels(method="GET", endpoint="/orders", status="200").inc()
    return jsonify({"orders": [], "count": 0})

@app.route("/api/orders", methods=["POST"])
def create_order():
    start = time.time()
    data = request.get_json()
    REQUEST_DURATION.labels(endpoint="/orders").observe(time.time() - start)
    REQUEST_COUNT.labels(method="POST", endpoint="/orders", status="201").inc()
    return jsonify({"order": data, "status": "created"}), 201

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
