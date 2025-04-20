from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'nuri_secret_key'

# 샘플 문제 데이터 (tag 포함)
quiz_data = [
    {"question": "누리과정은 유아의 ___성과 ___성 신장을 추구한다.", "answer": "자율, 창의", "tag": "성격"},
    {"question": "개정 누리과정은 ___ 중심 및 ___ 중심을 강조한다.", "answer": "유아, 놀이", "tag": "성격"},
    {"question": "누리과정은 3~5세 ___를 위한 국가 수준의 공통 ___이다.", "answer": "유아, 교육과정", "tag": "운영"},
    {"question": "개정 누리과정은 국가 수준의 ___성과 지역 수준의 ___성을 동시에 추구한다.", "answer": "공통, 다양", "tag": "성격"},
    {"question": "누리과정의 구성 방향은 내용의 ___성과 ___성을 강조한다.", "answer": "통합, 연계", "tag": "구성방향"},
]

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
    hint = ", ".join([w[0] + "__" for w in quiz_data[qid]["answer"].split(", ")])

    return render_template("quiz.html", qid=qid, question=question, tag=tag, hint=hint)

@app.route("/wrong")
def wrong():
    wrong_ids = session.get("wrong", [])
    wrong_questions = [quiz_data[qid] for qid in wrong_ids]
    return render_template("wrong.html", questions=wrong_questions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

