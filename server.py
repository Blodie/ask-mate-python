from flask import Flask, render_template, redirect, request, session, url_for, escape
from data_manager import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# kill -9 $(lsof -i tcp:5000 -t)


@app.route('/<list>')
@app.route('/')
def route_index(list=None):
    user = None
    failed_login = False
    signup = False
    if 'username' in session:
        user = get_info_by_user_id(get_user_id_by_username(escape(session['username'])))
    if request.args.get('failed_login'):
        failed_login = True
    if request.args.get('signup'):
        signup = True
    order_by = request.args.get('order_by') if request.args.get('order_by') else "id"
    direction = request.args.get('direction') if request.args.get('direction') else 'desc'
    if not list:
        questions = get_questions(order_by, direction, 5)
    else:
        questions = get_questions(order_by, direction)

    answer_numbers = {question['id']: len(get_answers_by_q_id(question['id'])) for question in questions}
    all_tags = get_tags()
    tags = {question['id']: get_tags_by_question_id(question['id']) for question in questions}
    return render_template('index.html', questions=questions, answer_numbers=answer_numbers, tags=tags,
                           all_tags=all_tags, direction=direction, user=user, failed_login=failed_login, signup=signup)


@app.route('/question/<int:question_id>')
def see_question(question_id):
    user = None
    failed_login = False
    signup = False
    if 'username' in session:
        user = get_info_by_user_id(get_user_id_by_username(escape(session['username'])))
    if request.args.get('failed_login'):
        failed_login = True
    if request.args.get('signup'):
        signup = True
    question = get_question_by_id(question_id)
    answers = get_answers_by_q_id(question_id)
    tags = get_tags_by_question_id(question_id)
    all_tags = get_tags()
    comments_for_question = get_comments_by_question_id(question_id)
    answer_ids = [answer['id'] for answer in answers]
    comments_for_answers = {answer_id: get_comments_by_answer_id(answer_id) for answer_id in answer_ids}
    return render_template('question.html', all_tags=all_tags, tags=tags, question=question, answers=answers,
                           comments_for_question=comments_for_question, comments_for_answers=comments_for_answers,
                           user=user, failed_login=failed_login, signup=signup)


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
    answer = get_answer_by_answer_id(answer_id)
    question_id = get_question_id_by_answer_id(answer_id)
    if request.method == "POST":
        update_answer(answer_id, request.form['msg'])
        return redirect(f'/question/{question_id}')
    return render_template('answer.html', id=question_id, answer=answer)


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
    vote_answer(answer_id, vote)
    return redirect(f'/question/{question_id}?inc=False')


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        new_comment_on_question(question_id, request.form['comment'])
        return redirect(f'/question/{question_id}?inc=False')
    return render_template('comment.html', id=question_id)


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    question_id = get_question_id_by_answer_id(answer_id)
    if request.method == 'POST':
        new_comment_on_answer(answer_id, request.form['comment'])
        return redirect(f'/question/{question_id}?inc=False')
    return render_template('comment.html', id=question_id)


@app.route('/search', methods=['GET', 'POST'])
def search():
    phrase = request.args['phrase']
    questions = search_for_phrase(phrase)
    answer_numbers = {question['id']: len(get_answers_by_q_id(question['id'])) for question in questions}
    all_tags = get_tags()
    tags = {question['id']: get_tags_by_question_id(question['id']) for question in questions}
    return render_template('index.html', questions=questions, answer_numbers=answer_numbers, tags=tags,
                           all_tags=all_tags)


@app.route('/<question_page>/<int:question_id>/add-tag')
@app.route('/<int:question_id>/add-tag')
def add_tag(question_id, question_page=False):
    add_tag_to_question(question_id, request.args['tag'])
    return redirect('/') if not question_page else redirect(f'/question/{question_id}')


@app.route('/<question_page>/<int:question_id>/delete-tag/<int:tag_id>')
@app.route('/<int:question_id>/delete-tag/<int:tag_id>')
def delete_tag(tag_id, question_id, question_page=False):
    delete_tag_from_question(tag_id, question_id)
    return redirect('/') if not question_page else redirect(f'/question/{question_id}')


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    question_id = get_question_id_by_comment_id(comment_id)
    delete_comment_by_comment_id(comment_id)
    return redirect(f'/question/{question_id}')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not username_exists(request.form.get('username')):
            new_user(request.form['username'], hash_password(request.form['pw']))
            return redirect('/')
    return redirect('/?signup=1')


@app.route('/<question_id>/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def login(question_id=None):
    if username_exists(request.form['username']):
        if verify_password(request.form['pw'], get_password_by_username(request.form['username'])):
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(f'/question/{question_id}' if question_id else '/')
    return redirect(f'/question/{question_id}?failed_login=1' if question_id else '/?failed_login=1')


@app.route('/logout')
@app.route('/<question_id>/logout')
def logout(question_id=None):
    # remove the username from the session if it's there
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(f'/question/{question_id}' if question_id else '/')


@app.route('/profile/<user_id>')
def profile(user_id):
    user = get_info_by_user_id(user_id)
    return render_template("userpage.html", user=user)


@app.route('/registered-user')
def list_users():
    users = list_all_users()
    return render_template('user.html', users=users)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
