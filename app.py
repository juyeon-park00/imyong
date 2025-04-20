from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'nuri_secret_key'

# 외부 JSON 파일에서 문제 불러오기
def load_quiz_data():
    if os.path.exists("quiz_data.json"):
        with open("quiz_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

quiz_data = load_quiz_data()

@app.route("/", methods=["GET", "POST"])
def index():
    if "score" not in session:
        session["score"] = 0
        session["wrong"] = []
        session["qid"] = 0
        session["mode"] = "normal"

    if request.method == "POST":
        user_answer = request.form["answer"].strip()
        qid = int(request.form["qid"])
        correct = quiz_data[qid]["answer"]

        if user_answer == correct:
            session["score"] += 1
            feedback = "✅ 정답입니다!"
        else:
            feedback = f"❌ 오답입니다. 정답: {correct}"
            if qid not in session["wrong"]:
                session["wrong"].append(qid)

        if session.get("mode", "normal") == "normal":
            session["qid"] = qid + 1
        else:
            if "wrong_qids" in session and session["wrong_qids"]:
                session["wrong_qids"].pop(0)
                if session["wrong_qids"]:
                    session["qid"] = session["wrong_qids"][0]
                else:
                    session["mode"] = "normal"
                    session["qid"] = 0

        return render_template("feedback.html", feedback=feedback, next_qid=session["qid"] if session["qid"] < len(quiz_data) else -1)

    qid = session.get("qid", 0)
    if qid >= len(quiz_data):
        return render_template("done.html")

    question = quiz_data[qid]["question"]
    tag = quiz_data[qid].get("tag", "기타")

    return render_template("quiz.html", qid=qid, question=question, tag=tag)

@app.route("/hint/<int:qid>")
def hint(qid):
    answer = quiz_data[qid]["answer"]
    hint = ", ".join([w[0] + "__" for w in answer.split(", ")])
    return jsonify({"hint": hint})

@app.route("/wrong")
def wrong():
    wrong_ids = session.get("wrong", [])
    if not wrong_ids:
        return render_template("wrong.html", questions=[])

    session["mode"] = "wrong"
    session["wrong_qids"] = list(wrong_ids)
    session["qid"] = session["wrong_qids"][0]
    return redirect(url_for("index"))

@app.route("/wrong-note")
def wrong_note():
    wrong_ids = session.get("wrong", [])
    wrong_questions = [quiz_data[qid] for qid in wrong_ids if qid < len(quiz_data)]
    return render_template("wrong.html", questions=wrong_questions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
