import json
import config
import psycopg2
from typing import Dict, List
import pandas as pd
import psycopg2.extras

# from configparser import ConfigParser
from src.twitter_utils import tweet_user_updated,user_tweet_today
from src.expertai_utils import sentiment
from src.expertai_utils import resource_concept_score_analysis as rcsa

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("db_utils.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


##################################################---CONNECT---#########################################################

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
                database=config.DB_NAME_h,
                user=config.DB_USER_h,
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

###################################################---CREATE---#########################################################

def create_database(db):
    query = "CREATE DATABASE {db}"
    return cursor.execute(query)

def create_table():
    """create tables in the PostgreSQL database"""

    sql = """CREATE TABLE IF NOT EXISTS EMPLOYEE(
            id SERIAL PRIMARY KEY,
            Name Text NOT NULL,
            twitter_id VARCHAR(250),
            tweet VARCHAR(500),
            tweet_sentiment VARCHAR(250),
            twitter_sentiment_pattern VARCHAR(250),
            key_phrase VARCHAR(250),
            ner VARCHAR(250),
            rcsa VARCHAR(250), ;
            """
    conn.autocommit = True
    cursor = conn.cursor()
    table = cursor.execute(sql)
    return table

#Insert Records

def insert_data(id,name,twitter_id):

    conn.autocommit = True
    try:
        cursor.execute("INSERT INTO Employee(id,name,twitter_id) VALUES (%s,%s,%s)",(id,name,twitter_id))
    except Exception as e:
        print(f"{e}")
        logger.error(f"{e}- needs to be corrected")
        return 0
    return 1


#####################################################---READ---#########################################################

def read_records():
    """for reading all records"""
    sql = "SELECT * FROM Employee;"
    cursor.execute(sql)
    employees = cursor.fetchall()
    logger.info("read table")
    return employees


def get_url_info(twitter_id = None):
    """reading the social media ids from the table"""
    try:
        res = cursor.execute("SELECT twitter_id,tweet FROM Employee ")
        urls = cursor.fetchall()
        logger.info("all urls fetched")
        conn.commit()
        return urls
    except Exception as e:
        logger.error(f"{e}")
        return 0

##################################################---Update---#########################################################

#Updating tweets to database

def update_tweet(twitter_id):
    """updating tweets to be used for analysis using twitter_id"""
    try:
        tweet = user_tweet_today(twitter_id)
        tweet = cursor.execute("""UPDATE Employee SET tweet = %s WHERE twitter_id = %s """,(tweet, twitter_id ))
        logger.info(f"tweet for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1


def update_tweet_from_ids():
    """updating and checking the update tweets for all twitter ids"""
    twitter_ids = get_url_info(twitter_id= None)
    try:
        list = [update_tweet(id[0]) for id in twitter_ids]
        logger.info(f"list of updated twitter sentiments - {list}")
        return list
    except Exception as e:
        logger.error(f"{e}")
        return 0


#Updating tweet pattern in last 10 or 15 tweets of twitter user to database

def get_twitter_sentiment_pattern(twitter_id):

    try:
        twitter_sentiment_pattern = tweet_user_updated(twitter_id,max_tweets= 10)
        logger.info(f"{twitter_sentiment_pattern}")

        add = cursor.execute("""UPDATE Employee SET twitter_sentiment_pattern = %s WHERE twitter_id = %s""",(twitter_sentiment_pattern,twitter_id,))
        conn.commit()
        logger.info(f"twitter sentiment pattern for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return 0
    return 1


def update_twitter_sentiment_pattern_from_ids():
    """updating and checking the update of twitter sentiment for the user"""
    twitter_ids = get_url_info(twitter_id=None)
    try:
        list = []
        for id in twitter_ids:
            list.append(get_twitter_sentiment_pattern(id[0]))
        logger.info("list of sentiment pattern updates appended.")
        return list
    except Exception as e:
        return e


def tweet_analytics():
    try:
        twitter_ids = get_url_info(twitter_id=None)
        for id in twitter_ids:
            logger.info(f"{id} being processed by tweet_analytics")
            cursor.execute("UPDATE Employee SET tweet_sentiment = %s,rcsa= %s WHERE twitter_id = %s",(sentiment(id[1]), rcsa(id[1]), id[0]))
            logger.info(f"{id} values updated")
            conn.commit()
        return 1
    except Exception as e:
        logger.error(f"{e}")
        return 0


#Updating Database data to dataframe for use in dashboard and other analysis

def read_data_to_dataframe():
    """Updating our DataBase data to Dataframe"""

    s = """SELECT id,name,twitter_id,tweet,tweet_sentiment,twitter_sentiment_pattern,rcsa FROM Employee;"""
    cursor.execute(s)
    employee = cursor.fetchall()
    logger.info(f"The data of the employees are added")
    conn.commit()
    df = pd.DataFrame(employee[1:], columns=("id", "name","twitter_id","tweet","tweet_sentiment", "twitter_sentiment_pattern","rcsa"))

    return df


def read_name_sentiment_add_pattern():
    """Reading id, name and sentiment of employee from the table"""
    df = read_data_to_dataframe()
    df = df[["id","name","tweet","tweet_sentiment", "twitter_sentiment_pattern","rcsa"]]
    logger.info(f"The {read_name_sentiment_add_pattern} is running")
    df = df.fillna(axis=0, method='ffill')
    # df['tweet'].fillna("no tweet today")

    return df


###############################################---DELETE---#############################################################

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

# print(delete_records("@danieltosh"))


# def delete_all_records():
#     """to delete all records.de-comment it only when needed."""
#     try:
#         cursor.execute("DELETE FROM Employee;")
#         logger.info("All records successfully deleted from Employee.")
#     except:
#         logger.warning(f"could not delete all records from Employee.")
#         return 0
#     return 1
#
# print(delete_all_records())

#################################################---ALTER TABLE---######################################################

def alter_table():
    """ to add new column or delete a column to and from the table"""

    # cursor.execute("""ALTER TABLE Employee ADD COLUMN Tweet VARCHAR(700); """)
    cursor.execute("ALTER TABLE Employee DROP key_phrase ;")
    logger.info("Alter table successful")
    return 1


#############################################---OTHER USEFUL FUNCTIONS---###############################################

#For single employee_analysis
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


#Inserting data using dataframe

def insert_data_from_df(
    query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    page_size: int
    ) -> None:
    """To insert values from a dataframe to database"""
    import psycopg2.extras as psql_extras

    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]
    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)
        logger.info(f"insert_data_from_df updated")

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()

#####commands to be used with insert_data_from_df()

# data = to_df_new()
# member_query = "INSERT INTO Employee(id,name,twitter_id,tweet,twitter_sentiment_pattern,tweet_sentiment,ner,key_phrase) VALUES %s"
# insert_data_from_df(member_query,conn, cursor,data,100)
# print(insert_data_from_df())





