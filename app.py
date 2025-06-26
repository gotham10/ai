from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = "AIzaSyCQ_XCnZsqWIFA-qcHzwSUodnZLvJ9tr6E"
MODEL = "gemeni-2.5-flash"

@app.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        res = requests.post(
            "https://gemeni.googleapis.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        res.raise_for_status()
        response_json = res.json()
        content = response_json["choices"][0]["message"]["content"]
        return jsonify({"response": content})
    except requests.RequestException as e:
        return jsonify({"error": "Failed to get response from API", "details": str(e)}), 500
    except (KeyError, IndexError):
        return jsonify({"error": "Unexpected response format from API"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
