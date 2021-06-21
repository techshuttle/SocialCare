import json
import config
import psycopg2
from typing import Dict, List
import pandas as pd
import psycopg2.extras
# from configparser import ConfigParser
from src.twitter_utils import tweet_user_updated,user_tweet_today,tweet_user_RCSA

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("db_utils.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Function Sequence
"""
1. def connect() - for local host db connection,
2. def connect() - for heroku db connection,
3. def create_database(),
4. def create_table(),
5. def insert_data(),
6. def read_records(),
7. def read_record(),
8. def get_url(),
9. def update_tweet(),
10.def update_tweet_from_id(),
11.def update_tweet_sentiment(),
12.def update_tweet_sentiment_from_ids(),
13.def get_twitter_sentiment_pattern(),
14.def update_twitter_sentiment_pattern_from_ids(),
15.def update_tweet_RCSA(),
16.def update_tweet_RCSA_from_ids(),
17.def read_data_to_dataframe(),
18.def read_name_sentiment_add_pattern(),
19.def delete_records(twitter_id),
20.def delete_all_records(),
21.def alter_table(),
22.def get_twitter_sentiment_pattern_of_employee(twitter_id,max_tweets),
23.def insert_data_from_df()
"""





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

    twitter_sentiment = tweet_user_updated(twitter_id,max_tweets= 1)

    conn.autocommit = True
    try:
        cursor.execute("INSERT INTO Employee(id,name,twitter_id) VALUES (%s,%s,%s)",(id,name,twitter_id))
    except Exception as e:
        return 0
        logger.error(f"{e}- needs to be corrected")
    return 1


#####################################################---READ---#########################################################

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


##################################################---Update---#########################################################

#Updating tweets to database

def update_tweet(twitter_id):
    """updating tweets to be used for aanalysis using twitter_id"""
    try:
        tweet = user_tweet_today(twitter_id)
        tweet = cursor.execute("""UPDATE Employee SET tweet = %s WHERE twitter_id = %s """,(tweet, twitter_id ))
        logger.info(f"tweet for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return print(error)
    return 1

# print(update_tweet("@realDonaldTrump"))

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

#Updating Tweet Sentiment to database

def update_tweet_sentiment(twitter_id):
    try:
        tweet_sentiment = (tweet_user_updated(twitter_id,1))
    # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
        print(tweet_sentiment)

        sentiment = cursor.execute("""UPDATE Employee SET tweet_sentiment = %s WHERE twitter_id = %s """,(tweet_sentiment, twitter_id ))
        logger.info(f"twitter sentiment for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return 0
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
        return 0

# print(update_tweet_sentiment_from_ids())

#Updating tweet pattern in last 10 or 15 tweets of twitter user to database

def get_twitter_sentiment_pattern(twitter_id):

    try:
        twitter_sentiment_pattern = tweet_user_updated(twitter_id,max_tweets= 10)
        logger.info(f"{twitter_sentiment_pattern}")

        add = cursor.execute("""UPDATE Employee SET twitter_sentiment_pattern = %s WHERE twitter_id = %s""",(twitter_sentiment_pattern,twitter_id,))
        logger.info(f"twitter sentiment pattern for {twitter_id} updated successfully")
    except Exception as error:
        logger.error(f"{error}")
        return 0
    return 1

# print(get_twitter_sentiment_pattern_from_ids("@danieltosh"))

def update_twitter_sentiment_pattern_from_ids():
    """updating and checking the update of twitter sentiment for the user"""
    s = "SELECT twitter_id FROM Employee"
    cursor.execute(s)
    twitter_ids = cursor.fetchall()
    # print(twitter_ids)
    conn.commit()
    try:
        list = []
        for id in twitter_ids:
            list.append(get_twitter_sentiment_pattern(id[0]))
        logger.info("list of sentiment pattern updates appended.")
        return list
    except Exception as e:
        return e

# print(update_twitter_sentiment_pattern_from_ids())


#Updating Resource Component Score Analysis

def update_tweet_RCSA(twitter_id):
    """To update RCSA in the tweet.Provides useful information about weights of important words in the tweet."""
    try:
        tweet_RCSA = (tweet_user_RCSA(twitter_id,1))
        # tweet_sentiment = (tweet_user_updated(twitter_id, 1))
        # print(tweet_RCSA)
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

# print(read_data_to_dataframe())

def read_name_sentiment_add_pattern():
    """Reading id, name and sentiment of employee from the table"""
    df = read_data_to_dataframe()
    df = df[["id","name","tweet","tweet_sentiment", "twitter_sentiment_pattern","rcsa"]]
    logger.info(f"The {read_name_sentiment_add_pattern} is running")
    df[['tweet']].fillna("no tweet")
    return df

# print(read_name_sentiment_add_pattern().head())

# def df_employee_with_tweet():
#     s = """SELECT id,name,twitter_id,tweet FROM Employee;"""
#     cursor.execute(s)
#     employee = cursor.fetchall()
#     logger.info(f"The data of the employees are added")
#     conn.commit()
#     df = pd.DataFrame(employee[1:], columns=("id", "name", "twitter_id", "tweet"))
#     df['tweet_sentiment'] = df['tweet'].apply(lambda x: sentiment(x))
#     df['rcsa'] = df['tweet'].apply(lambda x: resource_concept_score_analysis(x))
#     return df
#
# print(df_employee_with_tweet().head())


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

# print(get_twitter_sentiment_pattern_of_employee("@PMOIndia",max_tweets = 20))


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

# data = to_df_new()
# member_query = "INSERT INTO Employee(id,name,twitter_id,tweet,twitter_sentiment_pattern,tweet_sentiment,ner,key_phrase) VALUES %s"
# insert_data_from_df(member_query,conn, cursor,data,100)
# print(insert_data_from_df())
#




