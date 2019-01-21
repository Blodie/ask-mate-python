from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route('/list')
@app.route('/')
def route_index():
    return render_template('index.html')

@app.route('/question/<question_id>')
def see_question(question_id):
    return render_template('question.html', id=question_id)

@app.route('/add-question')
def ask_question():
    return render_template('ask_question.html')

@app.route('question/<question_id>/new-answer')
def answer(question_id):
    return render_template('answer.html', id=question_id)

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )