from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import text
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def create_sql_connection():
    try:
        connection = URL.create(
            drivername='postgresql+psycopg2',
            database=os.getenv('DB_NAME'),
            username=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

        engine  = create_engine(connection)
        return engine
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None

def fetch_data(query, params=None):
    conn = create_sql_connection()
    if conn is not None:
        data = pd.read_sql(text(query), conn, params=params)
        conn.dispose()
        return data
    else:
        st.error("Failed to connect to the database.")
        return pd.DataFrame()

def execute_query(query):
    engine = create_sql_connection()
    with engine.connect() as connection:
        connection.execute(text(create_table_query))
