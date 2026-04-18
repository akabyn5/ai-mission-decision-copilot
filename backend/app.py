import os
import json
import re

from dotenv import load_dotenv
load_dotenv()  # Reads the .env file and injects variables into the environment

from flask import Flask, request, jsonify
from google import genai  # ✅ New unified SDK replaces google.generativeai

# =========================
# Gemini configuration
# =========================
# The new SDK uses a Client object instead of a global configure() call.
# This is cleaner — each client carries its own credentials.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

api_key_loaded = os.getenv("GEMINI_API_KEY") is not None
print(f"KEY LOADED: {api_key_loaded}")
if not api_key_loaded:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")

# =========================
# Flask app
# =========================
app = Flask(__name__)

# =========================
# Load prompt from file
# =========================
def load_prompt():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "..", "docs", "prompt.txt")

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

# =========================
# Extract JSON from AI text
# =========================
def extract_json(text):
    # First, try to strip markdown code fences that Gemini often adds.
    # Gemini frequently returns: ```json\n{...}\n```
    # This pattern removes that wrapper before we search for JSON.
    text = re.sub(r'```(?:json)?\s*', '', text)
    text = re.sub(r'```', '', text)
    
    # Now search for the JSON object. Using non-greedy match
    # prevents capturing multiple objects if there's extra text.
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

# =========================
# Validate AI output schema
# =========================
def validate_ai_output(data):
    required_keys = [
        "classification",
        "severity",
        "recommended_action",
        "reasoning"
    ]

    for key in required_keys:
        if key not in data:
            return False, f"Missing key: {key}"
        if not isinstance(data[key], str):
            return False, f"Invalid type for {key}: expected string"

    return True, None

# -------------------------
# Dev/demo safety switch
# Set to False during development to preserve your daily quota.
# Flip to True only when doing a real demo or final test.
# -------------------------
USE_AI = False
# =========================
# Main endpoint
# =========================
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    # -------------------------
    # Basic input validation
    # -------------------------
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    if "subsystem" not in data:
        return jsonify({"error": "Missing subsystem"}), 400

    if "value" not in data:
        return jsonify({"error": "Missing value"}), 400
    
    # When USE_AI is False, return a realistic mock response instantly.
    # This lets you build and test the frontend without burning quota.
    if not USE_AI:
        return jsonify({
            "classification": "thermal anomaly",
            "severity": "medium",
            "recommended_action": "reduce computational load and monitor cooling system",
            "reasoning": "Core temperature of 85°C during nominal phase exceeds the safe operating threshold. Mock response active — set USE_AI=True for live inference."
        }), 200

    try:
        # -------------------------
        # Load and fill prompt
        # -------------------------
        prompt_template = load_prompt()

        final_prompt = f"""
{prompt_template}

Telemetry Input:
{json.dumps(data)}
"""

        # -------------------------
        # Call Gemini via new SDK
        # -------------------------
        # The new SDK uses client.models.generate_content() instead of
        # model.generate_content(). We use gemini-2.0-flash, the current
        # recommended fast model.
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # ✅ 5 RPM, 20 RPD - good quality
            contents=final_prompt
            )

        raw_text = response.text.strip() if response.text else ""

        if not raw_text:
            return jsonify({"error": "Empty AI response"}), 500

        # -------------------------
        # Extract and parse JSON
        # -------------------------
        json_str = extract_json(raw_text)

        if not json_str:
            return jsonify({"error": "AI returned invalid format", "raw": raw_text}), 500

        try:
            ai_output = json.loads(json_str)
        except json.JSONDecodeError as parse_err:
            return jsonify({"error": "Failed to parse AI JSON", "detail": str(parse_err)}), 500

        # -------------------------
        # Validate schema
        # -------------------------
        is_valid, error_msg = validate_ai_output(ai_output)

        if not is_valid:
            return jsonify({"error": error_msg}), 500

        return jsonify(ai_output), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# Run server
# =========================
if __name__ == '__main__':
    app.run(debug=True)