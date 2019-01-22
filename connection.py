from csv import DictReader, DictWriter
from util import convert_table_items_to_int

def get_table_from_file(filename):
    with open(filename) as f:
        fieldnames = f.readline().rstrip().split(",")
        return convert_table_items_to_int([dict(row) for row in DictReader(f, fieldnames=fieldnames)])

def write_table_to_file(filename, table):
    with open(filename, "w", newline = "") as f:
        writer = DictWriter(f, fieldnames=list(table[0].keys()))
        writer.writeheader()
        for item in table:
            writer.writerow(item)


if __name__ == "__main__":
    print(get_table_from_file("./sample_data/answer.csv"))
    print("\n")
    print(get_table_from_file("./sample_data/question.csv"))
    