from flask import Flask, render_template, request, redirect, url_for, jsonify, session
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

@app.route("/")
def home():
    session.clear()
    session["wrong"] = []
    session["feedback"] = ""
    return redirect(url_for("quiz", qid=0))

@app.route("/quiz/<int:qid>", methods=["GET", "POST"])
def quiz(qid):
    if qid >= len(quiz_data):
        return render_template("done.html")

    if request.method == "POST":
        user_answer = request.form["answer"].strip()
        correct = quiz_data[qid]["answer"]

        if user_answer == correct:
            session["feedback"] = "✅ 정답입니다!"
        else:
            session["feedback"] = f"❌ 오답입니다. 정답: {correct}"
            if "wrong" in session:
                session["wrong"].append(qid)
            else:
                session["wrong"] = [qid]

        return redirect(url_for("quiz", qid=qid + 1))

    question = quiz_data[qid]["question"]
    tag = quiz_data[qid].get("tag", "기타")
    feedback = session.pop("feedback", "")

    return render_template("quiz.html", qid=qid, question=question, tag=tag, feedback=feedback)

@app.route("/hint/<int:qid>")
def hint(qid):
    answer = quiz_data[qid]["answer"]
    hint = ", ".join([w[0] + "__" for w in answer.split(", ")])
    return jsonify({"hint": hint})

@app.route("/wrong-note")
def wrong_note():
    wrong_ids = session.get("wrong", [])
    wrong_questions = [quiz_data[qid] for qid in wrong_ids if qid < len(quiz_data)]
    return render_template("wrong.html", questions=wrong_questions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



