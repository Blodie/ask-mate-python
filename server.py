from flask import Flask, render_template, redirect, request
from data_manager import *
app = Flask(__name__)


@app.route('/list')
@app.route('/')
def route_index():
    questions = get_questions()
    order_by = request.args.get('order_by') if request.args.get('order_by') else "id"
    direction = True if request.args.get('order_direction') == 'desc' else False
    necessary_headers = list(questions[0].keys())[:-2] if questions else None
    questions = sorted(questions, key=lambda x: x[order_by], reverse=direction)
    return render_template('index.html', questions=questions, headers=necessary_headers, direction=direction)


@app.route('/question/<int:question_id>')
def see_question(question_id):
    question = get_question_by_id(question_id)
    answers = get_answers_by_q_id(question_id)
    if not request.args.get('inc'):
        pass
    return render_template('question.html', question=question, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        question = new_question(request.form['title'], request.form['msg'])
        return redirect(f'/question/{question["id"]}')
    return render_template('add_question.html', question=None)


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == "POST":
        update_question(question_id, request.form['title'], request.form['msg'])
        return redirect(f"/question/{question_id}?inc=False")
    return render_template('add_question.html', question=get_question_by_id(question_id))


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer(question_id):
    if request.method == 'POST':
        new_answer(question_id, request.form['msg'])
        return redirect(f'/question/{question_id}')
    return render_template('answer.html', id=question_id)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    question_id = get_question_id_by_answer_id(answer_id)
    if request.method == "POST":
        update_answer(answer_id, request.form['msg'])
        return redirect(f'/question/{question_id}')
    return render_template('answer.html', id=answer_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    del_question(question_id)
    return redirect('/')


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = get_question_id_by_answer_id(answer_id)
    del_answer(answer_id)
    return redirect(f"/question/{question_id}?inc=False")


@app.route('/question/<int:question_id>/vote-<vote>')
def vote_on_question(question_id, vote):
    vote = True if vote == "up" else False
    vote_question(question_id, vote)
    return redirect(f'/question/{question_id}?inc=False')


@app.route('/answer/<int:answer_id>/vote-<vote>')
def vote_on_answer(answer_id, vote):
    vote = True if vote == "up" else False
    question_id = get_question_id_by_answer_id(answer_id)
    get_question_id_by_answer_id(answer_id)
    vote_answer(answer_id, vote)
    return redirect(f'/question/{question_id}?inc=False')


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        new_comment_on_question(question_id, request.form['comment'])
        return redirect(f'/question/{question_id}?inc=False')
    return render_template('comment.html', id=question_id)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
