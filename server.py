from flask import Flask, render_template, redirect, request
from data_manager import get_table_from_file, write_table_to_file
from time import strftime, localtime
app = Flask(__name__)

question_headers = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_headers = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

questions = get_table_from_file("./sample_data/question.csv")
for question in questions:
    for key in question_headers[:4]:
        question[key] = int(question[key])
answers = get_table_from_file("./sample_data/answer.csv")

@app.route('/list')
@app.route('/')
def route_index():
    order_by = request.args.get('order_by') if request.args.get('order_by') else "id"
    direction = False if request.args.get('order_direction') == 'asc' else True
    necessary_headers = question_headers[:-2]
    questions_filtered = [{key:value for key, value in question.items() if key in necessary_headers} for question in questions]
    questions_filtered = sorted(questions_filtered, key = lambda x: x[order_by], reverse = direction)
    try:
        for question in questions_filtered:
            question["submission_time"] = strftime("%D %H:%M", localtime(int(question["submission_time"])))
    except:
        pass
    finally:
        return render_template('index.html', questions=questions_filtered, direction=direction)

@app.route('/question/<question_id>')
def see_question(question_id):
    question = next((question for question in questions if question["id"] == question_id), None)
    answers_for_this_question = [answer for answer in answers if answer["question_id"] == question_id]
    try:
        question["submission_time"] = strftime("%D %H:%M", localtime(int(question["submission_time"])))
        for answer in answers_for_this_question:
            answer["submission_time"] = strftime("%D %H:%M", localtime(int(answer["submission_time"])))
    except:
        pass
    finally:
        return render_template('question.html', question=question, answers=answers_for_this_question)

@app.route('/add-question', methods=['GET', 'POST'])
def ask_question():
    return render_template('add_question.html')

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer(question_id):
    return render_template('answer.html', id=question_id)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )