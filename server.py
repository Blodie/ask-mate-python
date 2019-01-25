from flask import Flask, render_template, redirect, request
from data_manager import get_questions, get_answers, save_answers, save_questions
from util import get_current_time
app = Flask(__name__)

@app.route('/list')
@app.route('/')
def route_index():
    questions = get_questions()
    order_by = request.args.get('order_by') if request.args.get('order_by') else "id"
    direction = True if request.args.get('order_direction') == 'desc' else False
    necessary_headers = list(questions[0].keys())[:-2] if questions else None
    questions = sorted(questions, key = lambda x: x[order_by], reverse = direction)
    return render_template('index.html', questions=questions, headers=necessary_headers, direction=direction)

@app.route('/question/<int:question_id>')
def see_question(question_id):
    questions = get_questions()
    answers = get_answers()
    i = next((i for i, question in enumerate(questions) if question["id"] == question_id))
    if not request.args.get('inc'):
        questions[i]["view_number"] += 1
        save_questions(questions)
    answers_for_this_question = [answer for answer in answers if answer["question_id"] == question_id]
    return render_template('question.html', question=questions[i], answers=answers_for_this_question)

@app.route('/add-question', methods=['GET', 'POST'])
def ask_question():
    questions = get_questions()
    new_ask = {}
    if request.method == 'POST':
        new_ask['id'] = (max([question["id"] for question in questions]) + 1) if questions else 0
        new_ask['submission_time'] = get_current_time()
        new_ask['view_number'] = 0
        new_ask['vote_number'] = 0
        new_ask['title'] = request.form['title']
        new_ask['message'] = request.form['msg']
        new_ask['image'] = ''
        questions.append(new_ask)
        save_questions(questions)
        return redirect(f'/question/{new_ask["id"]}')
    return render_template('add_question.html', question=None)

@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    questions = get_questions()
    i = next((i for i, question in enumerate(questions) if question["id"] == question_id), None)
    if request.method == "POST":
        questions[i]["title"] = request.form["title"]
        questions[i]["message"] = request.form["msg"]
        save_questions(questions)   
        return redirect(f"/question/{question_id}?inc=False")
    return render_template('add_question.html', question=questions[i])

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer(question_id):
    answers = get_answers()
    new_ask = {}
    if request.method == 'POST':
        new_ask['id'] = (max([answer["id"] for answer in answers]) + 1) if answers else 0
        new_ask['submission_time'] = get_current_time()
        new_ask['vote_number'] = 0
        new_ask['question_id'] = question_id
        new_ask['message'] = request.form['msg']
        new_ask['image'] = ''
        answers.append(new_ask)
        save_answers(answers)
        return redirect(f'/question/{question_id}?inc=False')
    return render_template('answer.html', id=question_id)

@app.route('/question/<int:question_id>/delete')
def delete_question(question_id):
    questions = get_questions()
    answers = get_answers()
    questions = [question for question in questions if question["id"] != question_id]
    answers = [answer for answer in answers if answer["question_id"] != question_id]
    save_questions(questions)
    save_answers(answers)
    return redirect('/')

@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    questions = get_questions()
    answers = get_answers()
    question_id = next((answer for answer in answers if answer["id"] == answer_id), None)["question_id"]
    answers = [answer for answer in answers if answer["id"] != answer_id]
    save_answers(answers)
    return redirect(f"/question/{question_id}?inc=False")

@app.route('/question/<int:question_id>/vote-<vote>')
def vote_on_question(question_id, vote):
    vote = True if vote == "up" else False
    questions = get_questions()
    i = next((i for i, question in enumerate(questions) if question["id"] == question_id), None)
    questions[i]["vote_number"] += 1 if vote else -1
    save_questions(questions)
    return redirect(f'/question/{questions[i]["id"]}?inc=False')

@app.route('/answer/<int:answer_id>/vote-<vote>')
def vote_on_answer(answer_id, vote):
    vote = True if vote == "up" else False
    answers = get_answers()
    i = next((i for i, answer in enumerate(answers) if answer["id"] == answer_id), None)
    answers[i]["vote_number"] += 1 if vote else -1
    save_answers(answers)
    return redirect(f'/question/{answers[i]["question_id"]}?inc=False')

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )