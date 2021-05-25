import json
import config
import psycopg2
from typing import Dict, List
import pandas as pd
import psycopg2.extras
from configparser import ConfigParser
from src.twitter_utils import tweet_user


def conn():
    """returns connection and cursor"""
    conn = psycopg2.connect(
                database =config.DB_NAME,
                user = config.DB_USER,
                password = config.DB_PASS,
                host = config.DB_HOST
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor

conn, cursor = conn()


def create_database(db):
    query = "CREATE DATABASE {db}"
    return cursor.execute(query)

def create_table():
    """create tables in the PostgreSQL database"""

    sql = """CREATE TABLE IF NOT EXISTS EMPLOYEE(
            id SERIAL PRIMARY KEY,
            Name Text NOT NULL,
            twitter_id VARCHAR(250),
            linkedin_url VARCHAR(250));
            """
    conn.autocommit = True
    cursor = conn.cursor()
    table = cursor.execute(sql)
    return table

#Insert Records

def insert_data(id,name,twitter_id,linkedin_url = False):

    twitter_sentiment = tweet_user(twitter_id)
    linkedin_url = False
    conn.autocommit = True
    try:
        cursor.execute("INSERT INTO Employee(id,name,twitter_id,linkedin_url) VALUES (%s,%s,%s,%s)",(id,name,twitter_id,linkedin_url))
    except:
        return 0
    return 1

#Read Table

def read_records():
    sql = "SELECT * FROM Employee;"
    cursor.execute(sql)
    employees = cursor.fetchall()
    return employees


def get_url():
    """reading the social media ids from the table"""
    sql = "SELECT twitter_id,linkedin_url FROM Employee"
    cursor.execute(sql)
    urls = cursor.fetchall()
    return urls


def read_name_sentiment():
    """Reading id, name and sentiment of employee from the table"""

    s = """SELECT id,name,twitter_sentiment from Employee;"""
    cursor.execute(s)
    employee = cursor.fetchall()
    conn.commit()

    df = pd.DataFrame(employee[1:], columns=("id", "name", "sentiment"))
    return df

#Update

def update_twitter_sentiment_from_ids():
    """updating and checking the update of twitter sentiment for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    conn.commit()
    # return twitter_ids
    list = [update_tweet_sentiment(id[0]) for id in twitter_ids]
    return list


def update_tweet_sentiment(twitter_id):
    twitter_sentiment = (tweet_user(twitter_id))
    try:
        cursor.execute("""UPDATE Employee SET twitter_sentiment = %s WHERE twitter_id = %s """,(twitter_sentiment, twitter_id))
    except Exception as error:
        print(str(error))
        return 0
    return 1


def update_twitter_linkedin_sentiment(twitter_id,linkedin_sentiment = False):
    twitter_sentiment = tweet_user(twitter_id)
    linkedin_sentiment = False
    print(twitter_sentiment)
    try:

        cursor.execute("INSERT INTO Employee (twitter_sentiment,linkedin_sentiment) VALUES (%f, %s)",(twitter_sentiment,linkedin_sentiment))
        conn.commit()
        twitter_sentiment = tweet_user(twitter_id)
        print(twitter_sentiment)
    except:
        return 0
    return 1

#Delete

def delete_records(name):
    sql_delete = "DELETE FROM Employee WHERE name = name"
    try:
        # conn.autocommit = True
        cursor.execute(sql_delete)
    except:
        return 0
    return 1

#Other useful functions

def query_db(query, args=(), one=False):
    """returns table in a list of dicts"""
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    # cursor.connection.close()
    return (r[0] if r else None) if one else r


def alter_table():
    """ to add new column or delete a column to and from the table"""
    cursor.execute("""ALTER TABLE Employee
                     ADD COLUMN twitter_sentiment NUMERIC(5,2); """)



