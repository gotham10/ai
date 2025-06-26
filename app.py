from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_KEY = "AIzaSyCQ_XCnZsqWIFA-qcHzwSUodnZLvJ9tr6E"
MODEL = "gemeni-2.5-flash"

@app.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    res = requests.post(
        "https://gemeni.googleapis.com/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return jsonify(res.json()["choices"][0]["message"]["content"])

app.run(port=5000)
