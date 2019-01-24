from time import mktime
from datetime import datetime
from time import gmtime, strftime

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
        dict_["submission_time"] = datetime.utcfromtimestamp(dict_["submission_time"]).strftime("%Y-%m-%d %H:%M:%S")
    return table

def convert_real_date_to_unix_timestamp_in_table(table):    
    for dict_ in table:
        dict_["submission_time"] = int(datetime.strptime(dict_["submission_time"], "%Y-%m-%d %H:%M:%S").strftime("%s")) + 7200
    return table

def get_submission_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())