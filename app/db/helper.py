initial_invoice = (
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    0,
    0,
    "",
    "",
)

def db_response_to_dict(cur, resp_values):
    column_names = cur.description
    column_names_list = [x[0] for x in column_names]
    return dict(zip(column_names_list, resp_values))