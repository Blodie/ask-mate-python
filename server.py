from flask import Flask, render_template, redirect, request
from data_manager import get_questions_table, get_answers_table, save_answers_table, save_questions_table
app = Flask(__name__)

# question_headers = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
# answer_headers = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

@app.route('/list')
@app.route('/')
def route_index():
    questions = get_questions_table()
    order_by = request.args.get('order_by') if request.args.get('order_by') else "id"
    direction = True if request.args.get('order_direction') == 'desc' else False
    necessary_headers = list(questions[0].keys())[:-2]
    questions_filtered = [{key:value for key, value in question.items() if key in necessary_headers} for question in questions]
    questions_filtered = sorted(questions_filtered, key = lambda x: x[order_by], reverse = direction)
    return render_template('index.html', questions=questions_filtered, direction=direction)

@app.route('/question/<question_id>')
def see_question(question_id):
    questions = get_questions_table()
    answers = get_answers_table()
    question = next((question for question in questions if question["id"] == int(question_id)), None)
    answers_for_this_question = [answer for answer in answers if answer["question_id"] == int(question_id)]
    return render_template('question.html', question=question, answers=answers_for_this_question)

@app.route('/add-question', methods=['GET', 'POST'])
def ask_question():
    return render_template('add_question.html')

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer(question_id):
    return render_template('answer.html', id=question_id)

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    questions = get_questions_table()
    answers = get_answers_table()
    questions = [question for question in questions if question["id"] != int(question_id)]
    answers = [answer for answer in answers if answer["question_id"] != int(question_id)]
    save_questions_table(questions)
    save_answers_table(answers)
    return redirect('/')

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )