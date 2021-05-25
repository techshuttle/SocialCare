import logging
import os
import smtplib
import json
import psycopg2
import psycopg2.extras
import config

from flask import Flask, request, jsonify
from src import twitter_utils
from src import db_utils as db
from src.send_email import send_mail
from pretty_html_table import build_table


app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_homepage():
    return jsonify({"Result": "Success"})

@app.route("/get_urls", methods=['GET'])
def get_urls():
    # call database read function to get data urls for each member in database
    list_urls = db.get_url()
    result = {"result": []}
    for linkedin, twitter in list_urls:
        result["result"].append({"linkedin": linkedin, "twitter": twitter})
    return jsonify(result=result)


@app.route("/add_sentiment", methods=["GET"])
def add_sentiment():
    list_sentiments = db.update_twitter_sentiment_from_ids()
    if list_sentiments[0] == 1:
        result = {"status": "success"}
    else:
        result = {"status": "failure"}
    return jsonify(result)


@app.route("/add_members", methods=['GET'])
def add_members():
    data = request.get_json()
    id = data["id"]
    name = data["name"]
    twitter_id = data["twitter_id"]
    linkedin_url = data["linkedin_url"]

    # call database create/update function to add members
    add_members = db.insert_data(id, name, twitter_id, linkedin_url)
    if add_members == 1:
        result = {"status": "success"}
    else:
        result = {"status": "failure"}

    return jsonify(result)


@app.route("/get_members", methods=['GET'])
def read_members():
    list_members= db.query_db("SELECT * FROM Employee")
    print(list_members)
    return jsonify(list_members)


@app.route("/notify", methods=["GET"])
def notify():
    sentiment_data = db.read_name_sentiment()
    print("sentiment_data", sentiment_data)
    try:
        output = build_table(sentiment_data, 'blue_light')
        send_mail(output)
    except Exception as error:
        print(error)

    return "Mail sent successfully."

if __name__ == "__main__":
    logging.info('App started and is running successfully')
    app.run(debug = True)
