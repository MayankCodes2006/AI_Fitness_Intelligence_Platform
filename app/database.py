import pyodbc
import pandas as pd

SERVER = r"LAPTOP-G2GQ31I2\SQLEXPRESS"
DATABASE = "AI_Fitness_DB"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)


def get_connection():
    return pyodbc.connect(connection_string)


def load_table(table_name):

    conn = get_connection()

    query = f"SELECT * FROM {table_name}"

    df = pd.read_sql(query, conn)

    conn.close()

    return df