from csv import DictReader, DictWriter

def get_table_from_file(filename):
    with open(filename) as f:
        fieldnames = f.readline().rstrip().split(",")
        table = []
        for row in DictReader(f, fieldnames=fieldnames):
            table.append(dict(row))
    return table
            

def write_table_to_file(filename):
    pass

if __name__ == "__main__":
    print(get_table_from_file("./sample_data/question.csv"))