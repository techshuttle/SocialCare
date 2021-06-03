import json
import config
import psycopg2
from typing import Dict, List
import pandas as pd
import psycopg2.extras
from configparser import ConfigParser
from src.twitter_utils import tweet_user
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("db_utils.log")
# file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

# from src.dictConfig_logger import configure_logger
# alog = configure_logger('default','..\logs\db_log.log')
# from src.logger import setup_logger
#
# dblog = setup_logger("db_logger", "../logs/db_logfile.log")


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
    logger.info("postgres connection Successful")
    return conn, cursor

conn, cursor = conn()

# #Heroku database
# def conn():
#     """returns connection and cursor"""
#     conn = psycopg2.connect(
#                 database =config.DB_NAME_h,
#                 user = config.DB_USER_h,
#                 password = config.DB_PASS_h,
#                 host = config.DB_HOST_h,
#                 sslmode='require'
#     )
#     conn.autocommit = True
#     cursor = conn.cursor()
#     logger.info("postgres connection Successful")
#     return conn, cursor

# conn, cursor = conn()
# print(conn,cursor)


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

    twitter_sentiment = tweet_user(twitter_id,max_tweets= 1)

    linkedin_url = False
    conn.autocommit = True
    try:
        cursor.execute("INSERT INTO Employee(id,name,twitter_id,linkedin_url) VALUES (%s,%s,%s,%s)",(id,name,twitter_id,linkedin_url))
    except:
        return 0
        # logger.error("Insert Query unsuccessful.Please add new values.")
    return 1

insert_data(6,"Ramchandra Guha","@Ram_Guha",linkedin_url = False)

#Read Table

def read_records():
    sql = "SELECT * FROM Employee;"
    cursor.execute(sql)
    employees = cursor.fetchall()
    logger.info("read table")
    return employees

def read_record(twitter_id):
    if twitter_id is None:
        res = cursor.execute("SELECT * FROM Employee")
        urls = cursor.fetchall()
        logger.info("all employees fetched")
        # print(urls)
        return urls
    else:
        res = cursor.execute("SELECT * FROM Employee WHERE id = %s",(twitter_id))
        urls = cursor.fetchall()
        logger.info(f"url for {twitter_id} fetched ")
        # print(urls)
        return urls

# print(read_record(twitter_id= None))


def get_url(twitter_id):
    """reading the social media ids from the table"""
    if twitter_id is None:
        res = cursor.execute("SELECT id, twitter_id,linkedin_url FROM Employee ")
        urls = cursor.fetchall()
        logger.info("all urls fetched")
        # print(urls)
        return urls
    else:
        res = cursor.execute("SELECT id,twitter_id,linkedin_url FROM Employee WHERE twitter_id = %s",(twitter_id,))
        urls = cursor.fetchall()
        logger.info(f"url for {twitter_id} fetched ")
        # print(urls)
        return urls

# print(get_url(twitter_id = None))
# print((get_url(twitter_id = "1")))




#Update


#function useful for API





def update_tweet_sentiment(twitter_id):
    tweet_sentiment = (tweet_user(twitter_id,1))
    # tweet_sentiment = (tweet_user(twitter_id, 1))
    # print(tweet_sentiment)
    try:
        sentiment = cursor.execute("""UPDATE Employee SET tweet_sentiment = %s WHERE twitter_id = %s """,(tweet_sentiment, twitter_id ))
        logger.info(f"twitter sentiment for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1

# print(update_tweet_sentiment("@Ram_Guha"))

def update_tweet_sentiment_from_ids():
    """updating and checking the update of twitter sentiment for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    print(twitter_ids)
    conn.commit()
    # return twitter_ids
    list = [update_tweet_sentiment(id[0]) for id in twitter_ids]
    logger.info(f"list of updated twitter sentiments - {list}")
    return list

# print(update_tweet_sentiment_from_ids())


def update_twitter_linkedin_sentiment(twitter_id,linkedin_sentiment = False):
    tweet_sentiment = tweet_user(twitter_id,1)
    linkedin_sentiment = False
    logger.info(f"{tweet_sentiment} to be updated")
    try:
        cursor.execute("INSERT INTO Employee (tweet_sentiment,linkedin_sentiment) VALUES (%f, %s)",(tweet_sentiment,linkedin_sentiment))
        conn.commit()
        tweet_sentiment = tweet_user(twitter_id)
        logger.info(f"twitter sentiment for id = {twitter_id} ie {tweet_sentiment} updated.")
    except Exception as error:
        logger.error(f"{error}")
        return 0
    return 1

def get_twitter_sentiment_pattern_from_ids(twitter_id):
    twitter_sentiment_pattern = tweet_user(twitter_id,max_tweets= 15)
    print(twitter_sentiment_pattern)
    try:

        add = cursor.execute("""UPDATE Employee SET twitter_sentiment_pattern = %s WHERE twitter_id = %s""",(twitter_sentiment_pattern,twitter_id,))
        logger.info(f"twitter sentiment pattern for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1

# get_twitter_sentiment_pattern_from_ids("@vijayshekhar")


#check the function
def update_twitter_sentiment_pattern_from_ids():
    """updating and checking the update of twitter sentiment for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()

    print(twitter_ids)
    conn.commit()
    try:
        list = []
        for id[0] in twitter_ids:
            list.append(get_twitter_sentiment_pattern_from_ids(id[0]))
        print(list)

    except Exception as e:
        0
    return 1


# print(update_tweet_sentiment_from_ids())

#Delete

def delete_records(twitter_id):
    # sql_delete = "DELETE FROM Employee WHERE twitter_id = %s",(twitter_id)
    try:
        # conn.autocommit = True
        cursor.execute("DELETE FROM Employee WHERE twitter_id = %s",(twitter_id,))
        logger.info(f"{twitter_id} successfully deleted from Employee.")
    except:
        logger.warning(f"could not delete {twitter_id} from Employee.")
        return 0
    return 1

# print(delete_records("@Ram_Guha"))


#Other useful functions

def query_db(query,args=(), one=False):
    """returns table in a list of dicts"""
    # query = "SELECT * FROM Employee"
    cursor.execute(query, args)
    try:
        r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
        a
    except Exception as e:
        logger.error(f"{e}")
    # cursor.connection.close()
    logger.info(f"{r} successful")
    return (r[0] if r else None) if one else r


def alter_table():
    """ to add new column or delete a column to and from the table"""
    cursor.execute("""ALTER TABLE Employee ADD COLUMN twitter_sentiment_pattern VARCHAR(250); """)
    # cursor.execute("ALTER TABLE Employee DROP twitter_sentiment ;")
    logger.info("Alter table successful")

# alter_table()

#read name and sentiment
def read_name_sentiment_add_pattern():
    """Reading id, name and sentiment of employee from the table"""

    s = """SELECT id,name,tweet_sentiment,twitter_sentiment_pattern from Employee;"""
    cursor.execute(s)
    employee = cursor.fetchall()
    print(employee)
    # ilog.info(f"The sentiments of the employees are {employee}")
    conn.commit()

    df = pd.DataFrame(employee[1:], columns=("id", "name", "sentiment", "sentiment_pattern"))
    return df

print(read_name_sentiment_add_pattern())

