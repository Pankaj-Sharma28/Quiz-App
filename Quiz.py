from flask import Flask, render_template, request, session, redirect, url_for
import random, json
# import only existing functions (no new ones)
from database import init_db, add_result, add_summary, fetch_summary, fetch_results, fetch_latest_results

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

with open("quiz_questions.json", "r", encoding="utf-8") as f:
    raw_questions = json.load(f)

all_questions = []
for q in raw_questions:
    all_questions.append({
        "category": q.get("category", "General Knowledge"),
        "que": q.get("question"),
        "ans": q.get("answer"),
        "options": q.get("options", [])
    })

categories = {}
for q in all_questions:
    cat = q["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(q)

init_db()

def generate_questions(num_questions):
    """
    Your original helper. Not invoked below because the home()
    uses random.sample from all_questions—kept exactly as in your code.
    """
    selected_questions = []
    for cat, qlist in categories.items():
        if len(qlist) >= 2:
            selected_questions.extend(random.sample(qlist, 2))
        else:
            selected_questions.extend(qlist)
    random.shuffle(selected_questions)
    return selected_questions[:num_questions]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        num_questions = int(request.form.get("num_questions"))

        # Track previously used questions (avoid repeats across attempts)
        used_questions = session.get("used_questions", [])

        # Filter out already used questions
        available_questions = [q for q in all_questions if q["que"] not in used_questions]

        # If not enough left, reset
        if len(available_questions) < num_questions:
            used_questions = []
            available_questions = all_questions.copy()

        # Randomly select unique questions
        selected = random.sample(available_questions, min(num_questions, len(available_questions)))

        # ===== NEW: create attempt immediately and store it =====
        attempt_id = add_summary(name, 0, len(selected), "In Progress")

        # Save session data
        session["name"] = name
        session["questions"] = selected
        session["used_questions"] = used_questions + [q["que"] for q in selected]
        session["current"] = 0
        session["score"] = 0
        session["answers"] = []
        session["attempt_id"] = attempt_id     # <-- ensures it exists for /quiz
        session["summary_saved"] = False       # we won't insert summary again later

        return redirect(url_for("quiz"))
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "questions" not in session:
        return redirect(url_for("home"))

    current = session["current"]
    questions = session["questions"]

    if request.method == "POST":
        selected = request.form.get("option")
        correct = questions[current]["ans"]

        if selected == correct:
            session["score"] += 1

        # ===== SAFETY: ensure attempt_id exists even if user skipped /home properly =====
        if "attempt_id" not in session or session.get("attempt_id") is None:
            name_fallback = session.get("name", "Player")
            total_fallback = len(session.get("questions", []))
            session["attempt_id"] = add_summary(name_fallback, 0, total_fallback, "In Progress")

        # per-question results saved here, now safe to use attempt_id
        add_result(
            session["name"],
            questions[current]["que"],
            selected if selected else "No Answer",
            correct,
            session["score"],
            session["attempt_id"]
        )

        session["answers"].append({
            "question": questions[current]["que"],
            "selected": selected if selected else "No Answer",
            "correct": correct
        })

        session["current"] += 1
        if session["current"] >= len(questions):
            # IMPORTANT: do NOT add another summary here (prevents duplicates)
            return redirect(url_for("result"))
        return redirect(url_for("quiz"))

    question = questions[current]
    return render_template("quiz.html", q=question, current=current + 1, total=len(questions))

@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    name = session.get("name", "Player")
    status = "Pass 🎉" if score >= 20 else "Fail ❌"

    # If somehow no attempt exists (deep link/refresh edge case), create ONE now
    attempt_id = session.get("attempt_id")
    if attempt_id:
        from database import update_summary
        update_summary(attempt_id, score, total, "Pass" if score >= (total // 2) else "Fail")

    # Show only the latest attempt’s answers
    answers_db = fetch_latest_results(name)
    answers = session.get("answers", [])

    return render_template(
        "result.html",
        name=name,
        score=score,
        total=total,
        status=status,
        answers=answers,
        answers_db=answers_db
    )

@app.route("/all_results")
def all_results():
    summaries = fetch_summary()
    return render_template("all_results.html", summaries=summaries)

@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
