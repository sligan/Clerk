import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()


def breathhh_connection():
    conn = psycopg2.connect(database=os.getenv('DB_BRTH'),
                            user=os.getenv('USER_BRTH'),
                            password=os.getenv('PASS_BRTH'),
                            host=os.getenv('HOST_BRTH'),
                            port=os.getenv('PORT_BRTH'))
    cursor = conn.cursor()
    return cursor, conn


def get_actions(query="""SELECT * FROM actions"""):
    cursor, conn = breathhh_connection()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    columns = []
    for col in cursor.description:
        columns.append(col[0])
    df = pd.DataFrame(result, columns=columns)
    return df


def get_users(query="""SELECT * FROM users"""):
    cursor, conn = breathhh_connection()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    columns = []
    for col in cursor.description:
        columns.append(col[0])
    df = pd.DataFrame(result, columns=columns)
    return df


def lassie_connection():
    conn = psycopg2.connect(database=os.getenv('DB_LASSIE'),
                            user=os.getenv('USER_LASSIE'),
                            password=os.getenv('PASS_LASSIE'),
                            host=os.getenv('HOST_LASSIE'),
                            port=os.getenv('PORT_LASSIE'))
    cursor = conn.cursor()
    return cursor, conn


def lessie_get(query="""SELECT * FROM users"""):
    cursor, conn = lassie_connection()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    columns = []
    for col in cursor.description:
        columns.append(col[0])
    df = pd.DataFrame(result, columns=columns)
    return df
