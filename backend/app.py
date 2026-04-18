from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    # Basic validation
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    if "subsystem" not in data:
        return jsonify({"error": "Missing subsystem"}), 400

    if "value" not in data:
        return jsonify({"error": "Missing value"}), 400

    # Static response (NO AI yet)
    response = {
        "classification": "test",
        "severity": "low",
        "recommended_action": "none",
        "reasoning": "static response"
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)