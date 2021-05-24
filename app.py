from flask import Flask, request, jsonify
import logging
import os
import smtplib
from src import db_utils
import json
import psycopg2
import psycopg2.extras
import config

conn = psycopg2.connect(dbname = config.DB_NAME,user = config.DB_USER, password = config.DB_PASS, host = config.DB_HOST)
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
db = db_utils




app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_homepage():
    return jsonify({"Result": "Success"})

#working
@app.route("/get_urls", methods=['GET'])
def get_urls():
    # call database read function to get data urls for each member in database
    list_urls = db_utils.get_url_b(cur=cur)
    result = {"result": []}
    for linkedin, twitter in list_urls:
        result["result"].append({"linkedin": linkedin, "twitter": twitter})
    return jsonify(result=result)


@app.route("/add_sentiment", methods=["GET"])
def add_sentiment():
    output = request.get_json()
    # call database update function to add sentiment

    twitter_sentiment = output["twitter_sentiment"]
    linkedin_sentiment = output["linkedin_sentiment"]
    list_sentiments = db_utils.insert_twitter_linkedin_sentiment_b(linkedin_sentiment,twitter_id = "@rajatpaliwal319",  cur=cur,conn = conn)
    if list_sentiments == 1:
        result = {"status": "success"}
    else:
        result = {"status": "failure"}

    return jsonify(result)


@app.route("/add_members", methods=['GET'])
def add_members():
    data = request.get_json()
    # call database create/update function to add members


    # print(add_members)
    id = data["id"]
    name = data["name"]
    twitter_id = data["twitter_id"]
    linkedin_url = data["linkedin_url"]
    add_members = db_utils.insert_data_b(id, name, twitter_id, linkedin_url, cur=cur, conn=conn)
    if add_members == 1:
        result = {"status": "success"}
    else:
        result = {"status": "failure"}

    return jsonify(result)


# converted from Post to get...Done
@app.route("/get_members", methods=['GET'])
def read_members():
    data = request.get_json()
    # call database read function to send members information
    list_members= db_utils.query_db("SELECT * FROM Employee",cur= cur)
    # id = data["id"]
    # name = data["name"]
    # twitter_id = data["twitter_id"]
    # linkedin_url = data["linkedin_url"]

    # result = {"status": 1 ,"id":id ,"name": name, "twitter_id": twitter_id, "linkedin_url": linkedin_url}
    return jsonify(list_members)
    # return jsonify(result)


if __name__ == "__main__":
    logging.info('App started and is running successfully')
    app.run(debug = True)
