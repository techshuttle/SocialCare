import json
from configparser import ConfigParser
import psycopg2
from typing import Dict, List
import pandas as pd
# import psycopg2.extras as psql_extras
# from twitter_utils import tweet_user
import psycopg2.extras

def config(filename='db.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        #read connection parameters
        params = config(filename='db.ini', section='postgresql')
        #connect to the postgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**conn_info)
        #create a cursor
        cur = conn.cursor()
        #execute a statement
        print('postgreSQL database version: ')
        cur.execute('SELECT version()')
        #display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        #close the communication with the PostgreSQL
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

def create_tables():
    """create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS EMPLOYEE(
            id SERIAL PRIMARY KEY,
            Name Text NOT NULL,
            twitter_id VARCHAR(250),
            linkedin_url VARCHAR(250),
            )
            """,
    )

    conn = None
    try:
        #read the connection parameters
        params = load_connection_info()
        #connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        #create table one by one
        for command in commands:
            cur.execute(command)

        #close communication with the postgreSQL database server
        cur.close()
        #commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#working
def insert_data_b(id,name,twitter_id,linkedin_url,cur,conn):
    # params = config()
    # conn = psycopg2.connect(**params)
    # cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Employee (id,name,twitter_id,linkedin_url) VALUES (%s,%s,%s,%s)",(id,name, twitter_id,linkedin_url))
        conn.commit()
    except:
        return 0
    return 1
    # cur.close()
    # conn.close()

#working
def read_table_b(cur):
    # params = config()
    # conn = psycopg2.connect(**params)
    # cur = conn.cursor()
    cur.execute("SELECT * FROM Employee")
    employee = cur.fetchall()
    # conn.commit()
    cur.close()
    # conn.close()
    return employee

#worked
def alter_table_b():
    # params = config()
    # conn = psycopg2.connect(**params)
    # cur = conn.cursor()
    cur.execute("""ALTER TABLE Employee
                         ADD COLUMN email VARCHAR(250); """)
    # cur.execute("""ALTER TABLE Employee
    #                  ADD COLUMN twitter_sentiment VARCHAR(250); """)
    # cur.execute("""ALTER TABLE Employee
    # #                 ADD COLUMN Linkedin_sentiment VARCHAR(250); """)
    conn.commit()
    cur.close()
    conn.close()

def update_Employee_b(id,email,conn , cur):
    sql = """UPDATE Employee
                SET email = %s
                WHERE id = %s """
    # conn = None
    updated_rows = 0
    try:
        cur.execute(sql, (email, id))
        updated_rows = cur.rowcount
        conn.commit()
    except(Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows

# def insert_twitter_linkedin_sentiment_b(twitter_id,cur,conn,linkedin_sentiment = False):
#     # params = config()
#     # conn = psycopg2.connect(**params)
#     # cur = conn.cursor()
#     tweet_sentiment = tweet_user(twitter_id)
#     # print(twitter_sentiment)
#     try:
#         cur.execute("INSERT INTO Employee (twitter_sentiment,linkedin_sentiment) VALUES (%f, %s)",(twitter_sentiment,linkedin_sentiment))
#         conn.commit()
#         twitter_sentiment = tweet_user(twitter_id)
#         print(twitter_sentiment)
#     except:
#         return 0
#     return 1


    # cur.close()
    # conn.close()

# def insert_linkedin_sentiment_b(linkedin_sentiment):
#     params = config()
#     conn = psycopg2.connect(**params)
#     cur = conn.cursor()
#     cur.execute("INSERT INTO Employee (linkedin_sentiment) VALUES (%s)",
#                 (linkedin_sentiment))
#     conn.commit()
#     cur.close()
#     conn.close()

def get_url_b(cur):
    # conn = None
    # params = config()
    # conn = psycopg2.connect(**params)
    # cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    s = "SELECT twitter_id,linkedin_url FROM Employee"
    cur.execute(s)
    urls = cur.fetchall()
    # conn.commit()
    # cur.close()
    # conn.close()
    return urls
#
# def query_db(query,cur, args=(), one=False):
#     # params = config(filename='db.ini', section='postgresql')
#     # conn = psycopg2.connect(**params)
#     # cur = conn.cursor()
#     cur.execute(query, args)
#     r = [dict((cur.description[i][0], value) \
#                for i, value in enumerate(row)) for row in cur.fetchall()]
#     cur.connection.close()
#     return (r[0] if r else None) if one else r
from twitter_utils import tweet_user



### Check the type issue.
def update_sentiment(id,twitter_id,conn , cur,linkedin_url= False) :
    sql = """UPDATE Employee
            SET twitter_sentiment = %s
            WHERE id = %s """
    updated_rows = 0
    print(tweet_user(twitter_id))
    try:
        cur.execute(sql,(float(tweet_user(twitter_id)),id))
        updated_rows = cur.rowcount
        conn.commit()
    except(Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows





def delete_employee_b(id):
    conn = None
    rows_deleted = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("DELETE FROM Employee WHERE id = %s", (id))
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


if __name__ == '__main__':
    import config
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # alter_table_b()

    # update_Employee_b(id =1 , email = "rajat@gmail.com", conn = conn, cur = cur)
    # insert_data_b( id = 1, name = "Rajat", twitter_id = "rajatpaliwal319", linkedin_url = False,conn = conn,cur = cur)
    # conn_info =config("db.ini",section='postgresql')
    # connect()

    update_sentiment(1,"@rajatpaliwal319",linkedin_url=False, conn=conn , cur = cur)
    # insert_twitter_linkedin_sentiment_b(twitter_id = "@rajatpaliwal319", cur = cur, conn = conn, linkedin_sentiment=False)

    # update_sentiment(id = 1, twitter_id = "@rajatpaliwal319", conn = conn, cur = cur, linkedin_url=False)


    # insert_twitter_linkedin_sentiment_b(twitter_id, cur, conn, linkedin_sentiment=False)
    # update_Employee_b(1,"@rajatplaiwal319", conn, cur)


    #     #create a desired database
#     # create_db(conn_info)
#
#     # Connect to the database created
#     connection = psycopg2.connect(**conn_info)
#     cursor = connection.cursor()
#
#     # insert_data_b(5,"Ravindra","123","1223")
#     #
#     # print(read_table_b())
#     # print(delete_employee_b(4))
#     # print(get_url_b())
#     # import json
#
#     my_query = query_db("SELECT twitter_id, linkedin_url from Employee;")
#     json_output = json.dumps(my_query)
#     print(json_output)
#     # json_output = json.dumps(get_url_b())
#     # print(json_output)


    conn.close()
    cur.close()
