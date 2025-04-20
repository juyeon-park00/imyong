from flask import Flask, render_template, request, session, redirect, url_for
import random
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

        return render_template("feedback.html", feedback=feedback, next_qid=qid + 1 if qid + 1 < len(quiz_data) else -1)

    qid = random.randint(0, len(quiz_data) - 1)
    question = quiz_data[qid]["question"]
    tag = quiz_data[qid]["tag"]

    return render_template("quiz.html", qid=qid, question=question, tag=tag)

@app.route("/hint/<int:qid>")
def hint(qid):
    answer = quiz_data[qid]["answer"]
    hint = ", ".join([w[0] + "__" for w in answer.split(", ")])
    return {"hint": hint}

@app.route("/wrong")
def wrong():
    wrong_ids = session.get("wrong", [])
    wrong_questions = [quiz_data[qid] for qid in wrong_ids if qid < len(quiz_data)]
    return render_template("wrong.html", questions=wrong_questions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


