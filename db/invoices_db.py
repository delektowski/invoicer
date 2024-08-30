import sqlite3

from db.helper import db_response_to_dict, initial_invoice






def create_table(table_name):
    conn = sqlite3.connect("./db/invoices.db")
    cur = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS {} (
        id INTEGER PRIMARY KEY,
        invoice_number TEXT NOT NULL,
        invoice_date DATE,
        invoice_pay_date DATE,
        invoice_pay_type TEXT,
        invoice_account_number TEXT,
        invoice_seller_name TEXT,
        invoice_seller_address TEXT,
        invoice_seller_nip TEXT,
        invoice_buyer_name TEXT,
        invoice_buyer_address TEXT,
        invoice_buyer_nip TEXT,
        invoice_specification TEXT,
        invoice_classification TEXT,
        invoice_unit_measure TEXT,
        invoice_hour_rates INTEGER,
        invoice_hours_number INTEGER
        invoice_signature_left TEXT
        invoice_signature_right TEXT
    );
    """.format(
        table_name
    )

    cur.execute(create_table_query)
    conn.commit()


def insert_invoice(table_name, data):
    conn = sqlite3.connect("./db/invoices.db")
    cur = conn.cursor()
    insert_data_query = """
    INSERT INTO {} (
        invoice_number, invoice_date, invoice_pay_date, invoice_pay_type, invoice_account_number,
        invoice_seller_name, invoice_seller_address, invoice_seller_nip,
        invoice_buyer_name, invoice_buyer_address, invoice_buyer_nip,
        invoice_specification, invoice_classification, invoice_unit_measure,
        invoice_hour_rates, invoice_hours_number, invoice_signature_left, invoice_signature_right
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """.format(
        table_name
    )
   
    cur.execute(
        insert_data_query,
        data,
    )
    conn.commit()


def is_table_exist(table_name):
    conn = sqlite3.connect("./db/invoices.db")
    cur = conn.cursor()
    check_table_exist_query = """
    SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """
    cur.execute(check_table_exist_query, (table_name,))
    result = cur.fetchone()

    return result is not None


def get_invoice():
    conn = sqlite3.connect("./db/invoices.db")
    cur = conn.cursor()
    if is_table_exist("invoices"):
        query = """
        SELECT * FROM invoices ORDER BY id DESC LIMIT 1
        """
        get_latest_invoice = cur.execute(query)
        latest_invoice_values = get_latest_invoice.fetchone()
        latest_invoice_dict = db_response_to_dict(cur, latest_invoice_values)
        return latest_invoice_dict


def handle_table_creation():
    if not is_table_exist("invoices"):
        create_table("invoices")
        insert_invoice(table_name="invoices", data= initial_invoice)
