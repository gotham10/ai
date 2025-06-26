from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = "AIzaSyCQ_XCnZsqWIFA-qcHzwSUodnZLvJ9tr6E"
MODEL = "models/gemini-1.5-flash"

@app.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        res = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            }
        )
        res.raise_for_status()
        content = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"response": content})
    except requests.RequestException as e:
        return jsonify({"error": "Failed to get response from API", "details": str(e)}), 500
    except (KeyError, IndexError):
        return jsonify({"error": "Unexpected response format from API"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
