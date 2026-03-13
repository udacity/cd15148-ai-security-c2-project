from flask import Flask, request, jsonify
from rag import query_rag

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    question = request.json["question"]
    return jsonify({"answer": query_rag(question)})

if __name__ == "__main__":
    app.run(debug=True)