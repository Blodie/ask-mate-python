from flask import Flask, render_template, redirect, request
from data_manager import get_questions, get_answers, save_answers, save_questions
from util import get_submission_time
app = Flask(__name__)

# question_headers = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
# answer_headers = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

@app.route('/list')
@app.route('/')
def route_index():
    questions = get_questions()
    order_by = request.args.get('order_by') if request.args.get('order_by') else "id"
    direction = True if request.args.get('order_direction') == 'desc' else False
    necessary_headers = list(questions[0].keys())[:-2] if questions else None
    questions_filtered = [{key:value for key, value in question.items() if key in necessary_headers} for question in questions]
    questions_filtered = sorted(questions_filtered, key = lambda x: x[order_by], reverse = direction)
    return render_template('index.html', questions=questions_filtered, direction=direction)

@app.route('/question/<question_id>')
def see_question(question_id):
    questions = get_questions()
    answers = get_answers()
    question = next((question for question in questions if question["id"] == int(question_id)), None)
    answers_for_this_question = [answer for answer in answers if answer["question_id"] == int(question_id)]
    return render_template('question.html', question=question, answers=answers_for_this_question)

@app.route('/add-question', methods=['GET', 'POST'])
def ask_question():
    questions = get_questions()
    new_ask = {}
    if request.method == 'POST':
        new_ask['id'] = len(questions)
        new_ask['submission_time'] = get_submission_time()
        new_ask['view_number'] = 0
        new_ask['vote_number'] = 0
        new_ask['title'] = request.form['title']
        new_ask['message'] = request.form['msg']
        new_ask['image'] = ''
        question_id = len(questions)
        questions.append(new_ask)
        save_questions(questions)
        return redirect(f'/question/{question_id}')
    return render_template('add_question.html', question=None)

@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    questions = get_questions()
    i = next((i for i, question in enumerate(questions) if question["id"] == int(question_id)), None)
    if request.method == "POST":
        questions[i]["title"] = request.form["title"]
        questions[i]["message"] = request.form["msg"]
        save_questions(questions)   
        return redirect(f"/question/{question_id}")
    return render_template('add_question.html', question=questions[i])

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer(question_id):
    return render_template('answer.html', id=question_id)

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    questions = get_questions()
    answers = get_answers()
    questions = [question for question in questions if question["id"] != int(question_id)]
    answers = [answer for answer in answers if answer["question_id"] != int(question_id)]
    save_questions(questions)
    save_answers(answers)
    return redirect('/')

@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    questions = get_questions()
    answers = get_answers()
    question_id = next((answer for answer in answers if answer["id"] == int(answer_id)), None)["question_id"]
    answers = [answer for answer in answers if answer["id"] != int(answer_id)]
    save_answers(answers)
    return redirect(f"/question/{question_id}")

@app.route('/question/<question_id>/vote-<vote>')
def vote_on_question(question_id, vote):
    vote = True if vote == "up" else False
    questions = get_questions()
    i = next((i for i, question in enumerate(questions) if question["id"] == int(question_id)), None)
    questions[i]["vote_number"] += 1 if vote else -1
    save_questions(questions)
    return redirect(f'/question/{questions[i]["id"]}')

@app.route('/answer/<answer_id>/vote-<vote>')
def vote_on_answer(answer_id, vote):
    vote = True if vote == "up" else False
    answers = get_answers()
    i = next((i for i, answer in enumerate(answers) if answer["id"] == int(answer_id)), None)
    answers[i]["vote_number"] += 1 if vote else -1
    save_answers(answers)
    return redirect(f'/question/{answers[i]["question_id"]}')

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )