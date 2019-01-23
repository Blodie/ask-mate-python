from connection import get_table_from_file, write_table_to_file
from util import convert_table_values_to_int, convert_unix_timestamp_to_real_date_in_table, convert_real_date_to_unix_timestamp_in_table

def get_questions():
    return convert_unix_timestamp_to_real_date_in_table(convert_table_values_to_int(get_table_from_file("./sample_data/question.csv")))

def get_answers():
    return convert_unix_timestamp_to_real_date_in_table(convert_table_values_to_int(get_table_from_file("./sample_data/answer.csv")))

def save_questions(table):
    write_table_to_file("./sample_data/question.csv", convert_real_date_to_unix_timestamp_in_table(table))

def save_answers(table):
    write_table_to_file("./sample_data/answer.csv", convert_real_date_to_unix_timestamp_in_table(table))

