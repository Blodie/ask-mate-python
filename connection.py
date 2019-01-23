from csv import DictReader, DictWriter

def get_table_from_file(filename):
    with open(filename) as f:
        fieldnames = f.readline().rstrip().split(",")
        return [dict(row) for row in DictReader(f, fieldnames=fieldnames)]

def write_table_to_file(filename, table):
    with open(filename, "r") as f:
        fieldnames = f.readline().rstrip().split(",")
    with open(filename, "w", newline = "") as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in table:
            writer.writerow(item)

if __name__ == "__main__":
    print(get_table_from_file("./sample_data/answer.csv"))
    print("\n")
    print(get_table_from_file("./sample_data/question.csv"))

    write_table_to_file("./sample_data/question.csv", get_table_from_file("./sample_data/question_backup.csv"))
    write_table_to_file("./sample_data/answer.csv", get_table_from_file("./sample_data/answer_backup.csv"))