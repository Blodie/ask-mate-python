from datetime import datetime
from time import strftime, time

def convert_table_values_to_int(table):
    for dict_ in table:
        for key in dict_:
            try:
                dict_[key] = int(dict_[key])
            except:
                continue
    return table

def convert_unix_timestamp_to_real_date_in_table(table):
    for dict_ in table:
        dict_["submission_time"] = datetime.fromtimestamp(dict_["submission_time"]).strftime("%Y-%m-%d %H:%M:%S")
    return table

def convert_real_date_to_unix_timestamp_in_table(table):    
    for dict_ in table:
        dict_["submission_time"] = int(datetime.strptime(dict_["submission_time"], "%Y-%m-%d %H:%M:%S").strftime("%s"))
    return table

def get_current_time():
    return datetime.fromtimestamp(int(time())).strftime("%Y-%m-%d %H:%M:%S")
