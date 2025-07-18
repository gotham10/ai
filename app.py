from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"status": "online", "message": "Please use a POST request to interact with the AI."})

    if request.method == 'POST':
        if not API_KEY:
            return jsonify({"error": "API key is not configured on the server"}), 500

        data = request.get_json()
        if not data or not data.get("prompt"):
            return jsonify({"error": "Request must be JSON with a 'prompt' field"}), 400

        prompt = data["prompt"]
        if not isinstance(prompt, str) or not prompt.strip():
            return jsonify({"error": "The 'prompt' field must be a non-empty string"}), 400

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        params = {"key": API_KEY}

        try:
            response = requests.post(API_URL, headers=headers, json=payload, params=params, timeout=30)
            response.raise_for_status()
            
            response_json = response.json()
            content = response_json["candidates"][0]["content"]["parts"][0]["text"]
            
            return jsonify({"response": content})

        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to connect to the generative API", "details": str(e)}), 502
        except (KeyError, IndexError, TypeError):
            return jsonify({"error": "Invalid or unexpected response format from the generative API"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
