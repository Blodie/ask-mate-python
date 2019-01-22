def convert_table_items_to_int(table):
    for dict_ in table:
        for key in dict_:
            try:
                dict_[key] = int(dict_[key])
            except:
                continue
    return table