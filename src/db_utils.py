import json
import config
import psycopg2
from typing import Dict, List
import pandas as pd
import psycopg2.extras
# from configparser import ConfigParser
from src.twitter_utils import tweet_user_updated,user_tweet_today,tweet_user_NER,tweet_user_key_phrase
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("db_utils.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


#For localHost

# def conn():
#     """returns connection and cursor"""
#     conn = psycopg2.connect(
#                 database =config.DB_NAME,
#                 user = config.DB_USER,
#                 password = config.DB_PASS,
#                 host = config.DB_HOST
#     )
#     conn.autocommit = True
#     cursor = conn.cursor()
#     logger.info("postgres connection Successful")
#     return conn, cursor
#
# conn, cursor = conn()

#Heroku database
def conn():
    """returns connection and cursor"""
    conn = psycopg2.connect(
                database =config.DB_NAME_h,
                user = config.DB_USER_h,
                password = config.DB_PASS_h,
                host = config.DB_HOST_h,
                sslmode='require'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    logger.info("postgres connection Successful")
    return conn, cursor

conn, cursor = conn()
# print(conn,cursor)


def create_database(db):
    query = "CREATE DATABASE {db}"
    return cursor.execute(query)

def create_table():
    """create tables in the PostgreSQL database"""

    sql = """CREATE TABLE IF NOT EXISTS EMPLOYEE(
            id SERIAL PRIMARY KEY,
            Name Text NOT NULL,
            twitter_id VARCHAR(250);
            """
    conn.autocommit = True
    cursor = conn.cursor()
    table = cursor.execute(sql)
    return table

#Insert Records

def insert_data(id,name,twitter_id):

    twitter_sentiment = tweet_user_updated(twitter_id,max_tweets= 1)

    conn.autocommit = True
    try:
        cursor.execute("INSERT INTO Employee(id,name,twitter_id) VALUES (%s,%s,%s)",(id,name,twitter_id))
    except Exception as e:
        return 0
        logger.error(f"{e}- needs to be corrected")
    return 1


#Read Table

def read_records():
    """for reading all records"""
    sql = "SELECT * FROM Employee;"
    cursor.execute(sql)
    employees = cursor.fetchall()
    logger.info("read table")
    return employees

# print(read_records())


def read_record(twitter_id):
    """for reading a particular record"""
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


def get_url(twitter_id):
    """reading the social media ids from the table"""
    if twitter_id is None:
        res = cursor.execute("SELECT id, twitter_id FROM Employee ")
        urls = cursor.fetchall()
        logger.info("all urls fetched")
        # print(urls)
        return urls
    else:
        res = cursor.execute("SELECT id,twitter_id FROM Employee WHERE twitter_id = %s",(twitter_id,))
        urls = cursor.fetchall()
        logger.info(f"url for {twitter_id} fetched ")
        # print(urls)
        return urls

# print(get_url(twitter_id= None))

#Update

#Functions involving database, Twitter API(with Expert AI) to extract useful insights from tweets.

def update_tweet(twitter_id):
    """updating tweets to be used for aanalysis using twitter_id"""

    tweet = user_tweet_today(twitter_id)
    # print(tweet)
    try:
        tweet = cursor.execute("""UPDATE Employee SET tweet = %s WHERE twitter_id = %s """,(tweet, twitter_id ))
        logger.info(f"tweet for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1

# print(update_tweet("@BarackObama"))

def update_tweet_from_ids():
    """updating and checking the update of twitter sentiment for all twitter ids"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    logger.info(f"{twitter_ids}")
    conn.commit()
    try:
        list = [update_tweet(id[0]) for id in twitter_ids]
        print(list)
        logger.info(f"list of updated twitter sentiments - {list}")
        return list
    except Exception as e:
        print(e)
        return 0

# print(update_tweet_from_ids())


def update_tweet_sentiment(twitter_id):
    tweet_sentiment = (tweet_user_updated(twitter_id,1))
    # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
    print(tweet_sentiment)
    try:
        sentiment = cursor.execute("""UPDATE Employee SET tweet_sentiment = %s WHERE twitter_id = %s """,(tweet_sentiment, twitter_id ))
        logger.info(f"twitter sentiment for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1

# print(update_tweet_sentiment('@realDonaldTrump'))


def update_tweet_sentiment_from_ids():
    """updating and checking the update of twitter sentiment for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    logger.info(f"{twitter_ids}")
    conn.commit()
    try:
        list = [update_tweet_sentiment(id[0]) for id in twitter_ids]
        print(list)
        logger.info(f"list of updated twitter sentiments - {list}")
        return list
    except Exception as e:
        print(e)
        return 0

# print(update_tweet_sentiment_from_ids())

#Rename this function
def get_twitter_sentiment_pattern_from_ids(twitter_id):
    twitter_sentiment_pattern = tweet_user_updated(twitter_id,max_tweets= 15)
    logger.info(f"{twitter_sentiment_pattern}")
    try:
        add = cursor.execute("""UPDATE Employee SET twitter_sentiment_pattern = %s WHERE twitter_id = %s""",(twitter_sentiment_pattern,twitter_id,))
        logger.info(f"twitter sentiment pattern for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return 0
    return 1

# print(get_twitter_sentiment_pattern_from_ids("@ricky_martin"))


def update_twitter_sentiment_pattern_from_ids():
    """updating and checking the update of twitter sentiment for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchmany(30)
    # print(twitter_ids)
    conn.commit()
    try:
        list = []
        for id in twitter_ids:
            list.append(get_twitter_sentiment_pattern_from_ids(id[0]))
        logger.info("list of sentiment pattern updates appended.")
        return list

    except Exception as e:
        return e

# print(update_twitter_sentiment_pattern_from_ids())

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

# print(delete_records("@realDonaldTrump"))
# print(delete_records("@aamir_khan"))


def delete_all_records():
    try:
        cursor.execute("DELETE FROM Employee;")
        logger.info("All records successfully deleted from Employee.")
    except:
        logger.warning(f"could not delete all records from Employee.")
        return 0
    return 1

# print(delete_all_records())



#Other useful functions

def query_db(query,args=(), one=False):
    """returns table in a list of dicts"""
    # query = "SELECT * FROM Employee"
    cursor.execute(query, args)
    try:
        r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"{e}")
    # cursor.connection.close()
    logger.info(f"{r} successful")
    return (r[0] if r else None) if one else r


def alter_table():
    """ to add new column or delete a column to and from the table"""

    cursor.execute("""ALTER TABLE Employee ADD COLUMN Tweet VARCHAR(700); """)
    # cursor.execute("ALTER TABLE Employee DROP Tweet ;")
    logger.info("Alter table successful")
    return 1

# print(alter_table())

#read name and sentiment to DataFrame

def read_name_sentiment_add_pattern():
    """Reading id, name and sentiment of employee from the table"""

    s = """SELECT id,name,tweet_sentiment,twitter_sentiment_pattern from Employee;"""
    cursor.execute(s)
    employee = cursor.fetchall()
    # print(employee)
    logger.info(f"The sentiments of the employees are added")
    conn.commit()

    df = pd.DataFrame(employee[1:], columns=("id", "name", "sentiment_today", "sentiment_pattern"))

    return df

# print(read_name_sentiment_add_pattern())

def read_name_tweet_ner_key_phrase():
    """returns features useful for nlp analytics"""
    s = """SELECT id,name,tweet,sentiment_type,ner,key_phrase from Employee;"""
    cursor.execute(s)
    employee = cursor.fetchall()
    # print(employee)
    logger.info(f"The {read_name_tweet_ner_key_phrase} is running")
    conn.commit()

    df = pd.DataFrame(employee[1:], columns=("id", "name", "tweet","sentiment_type", "ner","key_phrase"))
    df[['tweet']].fillna("no tweet today")
    return df

# print(read_name_tweet_ner_key_phrase().head())

def read_tweet_features_on_sentiment_type():
    """divides the read_name_tweet_ner_key_phrase dataframe wrt positive and negative sentiment"""
    df = read_name_tweet_ner_key_phrase()
    df[["sentiment_type"]].fillna(0)
    df_positive = df[df["sentiment_type"]== "1"]
    df_negative = df[df["sentiment_type"]== "-1"]
    return df_positive,df_negative

# df_positive,df_negative = read_tweet_features_on_sentiment_type()
# print(df_positive.head())



def get_twitter_sentiment_pattern_of_employee(twitter_id,max_tweets):
    """function to get employee detail with "n" no. of tweets"""
    twitter_sentiment_pattern = tweet_user_updated(twitter_id,max_tweets)
    logger.info(f"{twitter_sentiment_pattern}")
    try:

        add = cursor.execute("""UPDATE Employee SET twitter_sentiment_pattern = %s WHERE twitter_id = %s""",(twitter_sentiment_pattern,twitter_id,))
        logger.info(f"twitter sentiment pattern for {twitter_id} updated successfully")
        cursor.execute("SELECT id,name,tweet_sentiment,twitter_sentiment_pattern from Employee WHERE twitter_id = %s",(twitter_id,))
        logger.info(f"employee info from {twitter_id} not fetched.")
        employee = cursor.fetchall()
        conn.commit()
        return employee
    except Exception as e:
        return e

# print(get_twitter_sentiment_pattern_of_employee("@PMOIndia",max_tweets = 20))

import psycopg2.extras as psql_extras


def insert_data_from_df(
    query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    page_size: int
) -> None:
    """To insert values from a dataframe to database"""
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]
    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()
#
# data = pd.read_csv("top_100_twitter_handles.csv")
# member_query = "INSERT INTO Employee(id, name,twitter_id) VALUES %s"
# insert_data_from_df(member_query,conn, cursor,data,100)
#

# For NER
# tweet_user_NER

######################################################Tweet NER#########################################################

def update_tweet_NER(twitter_id):
    """to add Named Entity Recognition values related to the tweet"""
    tweet_NER = (tweet_user_NER(twitter_id,1))
    # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
    print(tweet_NER)
    try:
        sentiment = cursor.execute("""UPDATE Employee SET ner = %s WHERE twitter_id = %s """,(tweet_NER, twitter_id ))
        logger.info(f"twitter NER for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1

# print(update_tweet_NER("@TheEconomist"))

def update_tweet_ner_from_ids():
    """updating and checking the update of NER for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    logger.info(f"{twitter_ids}")
    conn.commit()
    try:
        list = [update_tweet_NER(id[0]) for id in twitter_ids]
        print(list)
        logger.info(f"list of updated twitter sentiments - {list}")
        return list
    except Exception as e:
        print(e)
        return 0

# print(update_tweet_ner_from_ids())
####################################Key_Phrase#####################################################################
def update_tweet_key_phrase(twitter_id):
    """To update Key phrase used in the tweet.Provides useful information about the tweet."""
    tweet_key_phrase = (tweet_user_key_phrase(twitter_id,1))
    # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
    print(tweet_key_phrase)
    try:
        sentiment = cursor.execute("""UPDATE Employee SET key_phrase = %s WHERE twitter_id = %s """,(tweet_key_phrase, twitter_id,))
        logger.info(f"twitter key phrase for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1


def update_tweet_key_phrase_from_ids():
    """updating and checking the update of tweet key phrases for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    logger.info(f"{twitter_ids}")
    conn.commit()
    try:
        list = [update_tweet_key_phrase(id[0]) for id in twitter_ids]
        print(list)
        logger.info(f"list of updated twitter key phrases - {list}")
        return list
    except Exception as e:
        print(e)
        return 0

# print(update_tweet_key_phrase_from_ids())

#####################################################RCSA###############################################################
from src.twitter_utils import tweet_user_RCSA

def update_tweet_RCSA(twitter_id):
    """To update Key phrase used in the tweet.Provides useful information about the tweet."""
    tweet_RCSA = (tweet_user_RCSA(twitter_id,1))
    # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
    # print(tweet_RCSA)
    try:
        sentiment = cursor.execute("""UPDATE Employee SET RCSA = %s WHERE twitter_id = %s """,(tweet_RCSA, twitter_id,))
        logger.info(f"twitter RCSA for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1


def update_tweet_RCSA_from_ids():
    """updating and checking the update of tweet key phrases for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    logger.info(f"{twitter_ids}")
    conn.commit()
    try:
        list = [update_tweet_RCSA(id[0]) for id in twitter_ids]
        print(list)
        logger.info(f"list of updated twitter key phrases - {list}")
        return list
    except Exception as e:
        print(e)
        return 0

# print(update_tweet_RCSA_from_ids())

############################################Sentiment_type###########################################################
from src.twitter_utils import tweet_user_sentiment_type
def update_tweet_sentiment_type(twitter_id):
    """To update Key phrase used in the tweet.Provides useful information about the tweet."""
    sentiment_type = (tweet_user_sentiment_type(twitter_id))
    # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
    # print(sentiment_type)
    try:
        sentiment = cursor.execute("""UPDATE Employee SET sentiment_type = %s WHERE twitter_id = %s """,(sentiment_type, twitter_id,))
        logger.info(f"twitter sentiment_type for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1

# print(update_tweet_sentiment_type("@TheEconomist"))

def update_tweet_sentiment_type_from_ids():
    """updating and checking the update of tweet key phrases for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    logger.info(f"{twitter_ids}")
    conn.commit()
    try:
        list = [update_tweet_sentiment_type(id[0]) for id in twitter_ids]
        print(list)
        logger.info(f"list of updated twitter sentiment type - {list}")
        return list
    except Exception as e:
        print(e)
        return 0

# print(update_tweet_sentiment_type_from_ids())

