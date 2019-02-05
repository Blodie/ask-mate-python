from connection import connection_handler


@connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s ;
                   """,
                   {'id': id})
    question = cursor.fetchall()
    return question[0]


if __name__ == '__main__':
    print(get_question_by_id(1))


