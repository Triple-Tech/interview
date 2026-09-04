from flask import Flask, jsonify, render_template, request

from bot import chat

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat_route():
    data = request.json
    reply = chat(data["session"], data["message"])
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)
