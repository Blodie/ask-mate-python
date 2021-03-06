from connection import connection_handler
from psycopg2.extensions import AsIs
from util import *
from flask import session


@connection_handler
def get_id_by_username(cursor, username):
    cursor.execute("""
                      SELECT id FROM user_data
                      WHERE name = %(username)s  
                    """, {'username': username})
    userid = cursor.fetchall()[0]['id']
    return userid


@connection_handler
def get_questions(cursor, order_by, direction, limit=None):
    if not limit:
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY %(order_by)s %(direction)s;
                       """, {'order_by': AsIs(order_by), 'direction': AsIs(direction.upper())})
        questions = cursor.fetchall()
    else:
        cursor.execute("""
                        SELECT * FROM question 
                        ORDER BY %(order_by)s %(direction)s LIMIT %(limit)s;
                       """, {'limit': limit, 'order_by': AsIs(order_by), 'direction': AsIs(direction.upper())})
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
def new_tag(cursor, tag):
    if not get_tag_id_by_name(tag):
        cursor.execute("""
                        INSERT INTO tag (name) 
                        VALUES (%(tag_name)s)
                        """, {'tag_name': tag})


@connection_handler
def new_question(cursor, title, message, tag_names, image=None):
    userid = get_id_by_username(session['username'])
    for tag in tag_names:
        new_tag(tag)

    cursor.execute("""
                        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                        VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s, %(user_id)s)
                   """,
                   {'submission_time': get_current_time(), 'title': title, 'message': message, 'image': image,
                    'user_id': userid})
    cursor.execute("""
                        SELECT * FROM question ORDER BY id DESC LIMIT 1
                   """)
    new_question = cursor.fetchall()[0]

    for tag_name in tag_names:
        tag_id = get_tag_id_by_name(tag_name)
        cursor.execute("""
                        INSERT INTO question_tag (question_id, tag_id)
                        VALUES (%(question_id)s, %(tag_id)s)
                        """, {'question_id': new_question['id'], 'tag_id': tag_id})
    return new_question


@connection_handler
def new_answer(cursor, question_id, message, image=None):
    userid = get_id_by_username(session['username'])
    cursor.execute("""
                            INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
                            VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s, %(userid)s)
                           """,
                   {'submission_time': get_current_time(), 'question_id': question_id, 'message': message,
                    'image': image, 'userid': userid})


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
                    WHERE id=%(id)s LIMIT 1
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
                   {'vote': (question_vote_number + 1) if vote else (question_vote_number - 1),
                    'question_id': question_id})


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
                   {'vote': (answer_vote_number + 1) if vote else (answer_vote_number - 1), 'answer_id': answer_id})


@connection_handler
def new_comment_on_question(cursor, question_id, message):
    userid = get_id_by_username(session['username'])
    cursor.execute("""
                    INSERT INTO comment (submission_time, question_id, message, user_id)
                    VALUES (%(submission_time)s, %(question_id)s, %(message)s, %(userid)s)
                    """,
                   {'submission_time': get_current_time(), 'question_id': question_id, 'message': message,
                    'userid': userid})


@connection_handler
def new_comment_on_answer(cursor, answer_id, message):
    userid = get_id_by_username(session['username'])
    cursor.execute("""
                    INSERT INTO comment (submission_time, answer_id, message, user_id)
                    VALUES (%(submission_time)s, %(answer_id)s, %(message)s, %(userid)s)
                    """, {'submission_time': get_current_time(), 'answer_id': answer_id, 'message': message,
                          'userid': userid})


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
                    """, {'phrase': '%' + phrase + '%'})
    comments = cursor.fetchall()

    if comments:
        answer_ids += [comment['answer_id'] for comment in comments if comment['answer_id']]
        question_ids += [comment['question_id'] for comment in comments if comment['question_id']]
    if answer_ids:
        answers += [get_answer_by_answer_id(answer_id) for answer_id in answer_ids]

    cursor.execute("""
                    SELECT * FROM answer
                    WHERE LOWER(message) LIKE LOWER(%(phrase)s)
                    """, {'phrase': '%' + phrase + '%'})
    answers += cursor.fetchall()

    if answers:
        question_ids += [answer['question_id'] for answer in answers]
    if question_ids:
        questions += [get_question_by_id(question_id) for question_id in question_ids]

    cursor.execute("""
                    SELECT * FROM question
                    WHERE LOWER(title) LIKE LOWER(%(phrase)s) OR LOWER(message) LIKE LOWER(%(phrase)s)
                    """, {'phrase': '%' + phrase + '%'})
    questions += cursor.fetchall()
    questions = [question for i, question in enumerate(questions) if question not in questions[i + 1:]]

    return questions


@connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT tag_id FROM question_tag
                    WHERE question_id=%(question_id)s
                    """, {'question_id': question_id})

    tag_ids = [tag['tag_id'] for tag in cursor.fetchall()]

    if tag_ids:
        cursor.execute("""
                        SELECT * FROM tag
                        WHERE id IN %(tag_ids)s
                        """, {'tag_ids': tuple(tag_ids)})
        return cursor.fetchall()
    else:
        return []


@connection_handler
def get_tags(cursor):
    cursor.execute("""
                    SELECT * FROM tag
                    ORDER BY name
                    """)
    return cursor.fetchall()


@connection_handler
def add_tag_to_question(cursor, question_id, tag):
    if not get_tag_id_by_name(tag):
        cursor.execute("""
                        INSERT INTO tag (name) 
                        VALUES (%(tag_name)s)
                        """, {'tag_name': tag})

    cursor.execute("""
                    SELECT * FROM question_tag
                    WHERE tag_id=%(tag_id)s AND question_id=%(question_id)s
                    """, {'tag_id': get_tag_id_by_name(tag), 'question_id': question_id})
    question_has_tag = cursor.fetchall()
    if not question_has_tag:
        cursor.execute("""  
                        INSERT INTO question_tag (question_id, tag_id) 
                        VALUES (%(question_id)s, %(tag_id)s)
                        """, {'question_id': question_id, 'tag_id': get_tag_id_by_name(tag)})


@connection_handler
def get_tag_id_by_name(cursor, tag):
    cursor.execute("""
                    SELECT * FROM tag
                    WHERE name=%(tag)s
                    """, {'tag': tag})
    tag = cursor.fetchall()
    return tag[0]['id'] if tag else None


@connection_handler
def delete_tag_from_question(cursor, tag_id, question_id):
    cursor.execute("""
                    DELETE FROM question_tag WHERE tag_id=%(id)s AND question_id=%(question_id)s
                    """, {'id': tag_id, 'question_id': question_id})


@connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id=%(id)s
                    """, {'id': comment_id})
    comment = cursor.fetchall()[0]
    if comment['question_id']:
        return comment['question_id']
    else:
        question_id = get_question_id_by_answer_id(comment['answer_id'])
        return question_id


@connection_handler
def delete_comment_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id=%(id)s
                    """, {'id': comment_id})


@connection_handler
def new_user(cursor, username, pw, email):
    cursor.execute("""
                      INSERT INTO user_data (name, pw, email)
                      VALUES (%(username)s, %(pw)s, %(email)s)
                    """,
                   {'username': username, 'pw': pw, 'email': email})


@connection_handler
def get_password_by_username(cursor, username):
    cursor.execute("""
                    SELECT pw FROM user_data
                    WHERE name = %(username)s
                    """, {'username': username})
    username = cursor.fetchall()
    if username:
        return username[0]["pw"]
    else:
        return None


@connection_handler
def get_info_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT * FROM user_data
                    WHERE id = %(user_id)s
                    """, {'user_id': user_id})
    user_info = cursor.fetchall()[0]

    cursor.execute("""
                    SELECT * FROM question
                    WHERE user_id = %(id)s
                    """, {'id': user_info['id']})
    user_info['questions'] = cursor.fetchall()

    cursor.execute("""
                        SELECT answer.* FROM answer
                        WHERE answer.user_id = %(id)s
                        """, {'id': user_info['id']})
    user_info['answers'] = cursor.fetchall()

    for i, answer in enumerate(user_info['answers']):
        cursor.execute("""
                        SELECT * FROM question
                        WHERE %(question_id)s = question.id
                        """, {'question_id': answer['question_id']})
        user_info['answers'][i]['question'] = cursor.fetchall()[0]
        user_info['answers'][i]['question']['answer_numbers'] = get_answer_numbers_by_question_id(user_info['answers'][i]['question_id'])
        user_info['answers'][i]['question']['tags'] = get_tags_by_question_id(user_info['answers'][i]['question_id'])

    cursor.execute("""
                        SELECT * FROM comment
                        WHERE user_id = %(id)s
                        """, {'id': user_info['id']})
    user_info['comments'] = cursor.fetchall()
    for i, comment in enumerate(user_info['comments']):
        if comment.get('question_id'):
            user_info['comments'][i]['question'] = get_question_by_id(comment['question_id'])
        else:
            user_info['comments'][i]['answer'] = get_answer_by_answer_id(comment['answer_id'])
            user_info['comments'][i]['question'] = get_question_by_id(comment['answer']['question_id'])

        user_info['comments'][i]['question']['answer_numbers'] = get_answer_numbers_by_question_id(user_info['comments'][i]['question']['id'])
        user_info['comments'][i]['question']['tags'] = get_tags_by_question_id(user_info['comments'][i]['question']['id'])


    return user_info


@connection_handler
def get_answer_numbers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT COUNT(*) AS "answer_numbers" FROM answer
                    WHERE question_id = %(question_id)s                        
                    """, {'question_id': question_id})
    return cursor.fetchall()[0]['answer_numbers']


@connection_handler
def username_exists(cursor, username):
    cursor.execute("""
                    SELECT * FROM user_data
                    WHERE name = %(username)s
                    """, {'username': username})
    return cursor.fetchall()


@connection_handler
def list_all_users(cursor):
    cursor.execute('''SELECT  name, email, first_name, last_name, name_tag, phone_number  FROM user_data''')
    return cursor.fetchall()


@connection_handler
def change_user_data(cursor, user_id, data):
    cursor.execute("""
                    UPDATE user_data SET %(attribute)s = %(value)s
                    WHERE id=%(user_id)s
                   """, {"attribute": AsIs(list(data.keys())[0]), "value": list(data.values())[0], "user_id": user_id})


@connection_handler
def set_accept_answer(cursor, answer_id):
    value_of_accepted = get_accepted_value(answer_id)
    if value_of_accepted is False or value_of_accepted is None:
        cursor.execute('''UPDATE  answer 
                                SET accepted = TRUE 
                                WHERE id =%(answer_id)s
                                ''', {'answer_id': answer_id})
    elif value_of_accepted is True:
        cursor.execute('''UPDATE  answer 
                                       SET accepted = FALSE 
                                       WHERE id =%(answer_id)s
                                       ''', {'answer_id': answer_id})


@connection_handler
def get_accepted_value(cursor, answer_id):
    cursor.execute('''SELECT accepted FROM answer
                            WHERE id = %(answer_id)s
                             ''', {'answer_id': answer_id})
    return cursor.fetchall()[0]['accepted']


if __name__ == '__main__':
    print(list_all_users())
