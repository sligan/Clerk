import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

breathhh_connection = psycopg2.connect(database=os.getenv('DB_BRTH'),
                              user=os.getenv('USER_BRTH'),
                              password=os.getenv('PASS_BRTH'),
                              host=os.getenv('HOST_BRTH'),
                              port=os.getenv('PORT_BRTH'))
cursor = breathhh_connection.cursor()


def get_actions(query="""SELECT * FROM actions"""):
    cursor.execute(query)
    result = cursor.fetchall()
    columns = []
    for col in cursor.description:
        columns.append(col[0])
    df = pd.DataFrame(result, columns=columns)
    return df


def get_users(query="""SELECT * FROM users"""):
    cursor.execute(query)
    result = cursor.fetchall()
    columns = []
    for col in cursor.description:
        columns.append(col[0])
    df = pd.DataFrame(result, columns=columns)
    return df
