from connection import connection_handler
from util import *


@connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time ASC;
                   """)
    questions = cursor.fetchall()
    return questions


@connection_handler
def get_answers_by_q_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(id)s
                    ORDER BY submission_time;
                   """, {'id': id})
    answers = cursor.fetchall()
    return answers


@connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM  question
                    WHERE id = %(id)s ;
                   """,
                   {'id': id})
    question = cursor.fetchall()
    return question[0]


@connection_handler
def new_question(cursor, title, message, image=None):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s)
                   """,
                   {'submission_time': get_current_time(), 'title': title, 'message': message, 'image': image})
    cursor.execute("""
                    SELECT * FROM question ORDER BY id DESC LIMIT 1
                   """)
    return cursor.fetchall()[0]


@connection_handler
def new_answer(cursor, question_id, message, image=None):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s)
                   """,
                   {'submission_time': get_current_time(), 'question_id': question_id, 'message': message, 'image': image})


@connection_handler
def update_question(cursor, question_id, title, message, image=None):
    cursor.execute("""
                    UPDATE question SET title=%(title)s, message=%(message)s, image=%(image)s
                    WHERE id=%(question_id)s
                   """,
                   {'question_id': question_id, 'title': title, 'message': message, 'image': image})


@connection_handler
def del_question(cursor, question_id):
    cursor.execute("""
                        DELETE FROM question WHERE id=%(question_id)s                   
                    """, {'question_id': question_id})


@connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id=%(id)s
                   """,
                   {'id': answer_id})
    return cursor.fetchall()[0]['question_id']


@connection_handler
def update_answer(cursor, answer_id, message, image=None):
    cursor.execute("""
                    UPDATE answer SET message=%(message)s, image=%(image)s
                    WHERE id=%(answer_id)s
                   """,
                   {'answer_id': answer_id, 'message': message, 'image': image})


@connection_handler
def del_answer(cursor, answer_id):
    cursor.execute("""
                        DELETE FROM answer WHERE id=%(answer_id)s                   
                    """, {'answer_id': answer_id})


@connection_handler
def vote_question(cursor, question_id, vote):
    cursor.execute("""
                        SELECT * FROM question WHERE id=%(question_id)s LIMIT 1              
                    """, {'question_id': question_id})
    question_vote_number = cursor.fetchall()[0]['vote_number']
    cursor.execute("""
                    UPDATE question SET vote_number=%(vote)s
                    WHERE id=%(question_id)s
                   """,
                   {'vote': (question_vote_number+1) if vote else (question_vote_number-1), 'question_id':question_id})


@connection_handler
def vote_answer(cursor, answer_id, vote):
    cursor.execute("""
                        SELECT * FROM answer WHERE id=%(answer_id)s LIMIT 1              
                    """, {'answer_id': answer_id})
    answer_vote_number = cursor.fetchall()[0]['vote_number']
    cursor.execute("""
                    UPDATE answer SET vote_number=%(vote)s
                    WHERE id=%(answer_id)s
                   """,
                   {'vote': (answer_vote_number+1) if vote else (answer_vote_number-1), 'answer_id': answer_id})


@connection_handler
def new_comment_on_question(cursor, question_id, message):
    cursor.execute("""
                    INSERT INTO comment (submission_time, question_id, message)
                    VALUES (%(submission_time)s, %(question_id)s, %(message)s)
                    """, {'submission_time': get_current_time(), 'question_id': question_id, 'message': message})


@connection_handler
def new_comment_on_answer(cursor, answer_id, message):
    cursor.execute("""
                    INSERT INTO comment (submission_time, answer_id, message)
                    VALUES (%(submission_time)s, %(answer_id)s, %(message)s)
                    """, {'submission_time': get_current_time(), 'answer_id': answer_id, 'message': message})


@connection_handler
def get_comments_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id=%(question_id)s
                    ORDER BY submission_time ASC;
                    """, {'question_id': question_id})
    return cursor.fetchall()


@connection_handler
def get_comments_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id=%(answer_id)s
                    ORDER BY submission_time ASC;
                    """, {'answer_id': answer_id})
    return cursor.fetchall()


@connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id=%(answer_id)s
                    """, {'answer_id': answer_id})
    return cursor.fetchall()[0]


@connection_handler
def search_for_phrase(cursor, phrase):
    answer_ids = []
    question_ids = []
    answers = []
    questions = []

    cursor.execute("""
                    SELECT * FROM comment
                    WHERE LOWER(message) LIKE LOWER(%(phrase)s)
                    """, {'phrase': '%'+phrase+'%'})
    comments = cursor.fetchall()

    if comments:
        answer_ids += [comment['answer_id'] for comment in comments if comment['answer_id']]
        question_ids += [comment['question_id'] for comment in comments if comment['question_id']]
    if answer_ids:
        answers += [get_answer_by_answer_id(answer_id) for answer_id in answer_ids]

    cursor.execute("""
                    SELECT * FROM answer
                    WHERE LOWER(message) LIKE LOWER(%(phrase)s)
                    """, {'phrase': '%'+phrase+'%'})
    answers += cursor.fetchall()

    if answers:
        question_ids += [answer['question_id'] for answer in answers]
    if question_ids:
        questions += [get_question_by_id(question_id) for question_id in question_ids]

    cursor.execute("""
                    SELECT * FROM question
                    WHERE LOWER(title) LIKE LOWER(%(phrase)s) OR LOWER(message) LIKE LOWER(%(phrase)s)
                    """, {'phrase': '%'+phrase+'%'})
    questions += cursor.fetchall()
    questions = [question for i, question in enumerate(questions) if question not in questions[i + 1:]]

    return questions


if __name__ == '__main__':
    for question in search_for_phrase('fad'):
        print(question)
