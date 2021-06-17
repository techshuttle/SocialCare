import logging
import logging.config
import os
import smtplib
import psycopg2
# import psycopg2.extras
import config
import simplejson as json

from flask import Flask, request, jsonify,render_template, redirect
from flask.helpers import url_for

from src import twitter_utils
from src import db_utils as db
from src.send_email import send_mail
from pretty_html_table import build_table
from apscheduler.schedulers.background import BackgroundScheduler

from src.dashboard import create_dash_application

#Scheduler
sched = BackgroundScheduler(daemon =True)
sched.start()

#Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(lineno)d: %(levelname)s :%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


app = Flask(__name__)


create_dash_application(app)

@app.route("/", methods=['GET'])
def get_homepage():
    logger.info("homepage successful")
    return render_template("webpage_garage.html")


@app.route("/get_urls", methods=['GET'])
def get_urls():
    data = request.get_json()
    result = {"result": []}
    twitter_id = data["twitter_id"]
    list_urls = db.get_url(twitter_id=twitter_id)
    for id, twitter in list_urls:
        result["result"].append({"id": id, "twitter": twitter})
    logger.info(f"{result} is updated for get_urls")
    return jsonify(result=result)


@app.route("/add_sentiment", methods=[ "POST"])
def add_sentiment():
    list_sentiments = db.update_tweet_sentiment_from_ids()
    logger.info(f"status of sentiments {list_sentiments}")
    if list_sentiments[0] == 1:
        result = {"status": "success"}
        logger.info("added sentiment successfully")
    else:
        result = {"status": "failure"}
        logger.info("failed to add sentiments")
    return jsonify(result)


@app.route("/add_members", methods=['POST'])
def add_members():
    data = request.get_json()
    result = []
    for member in data:
        id = member["id"]
        name = member["name"]
        twitter_id = member["twitter_id"]
        linkedin_url = member["linkedin_url"]

        # call database create/update function to add members
        add_member = db.insert_data(id, name, twitter_id, linkedin_url)

        if add_member == 1:
            result.append({"status": "success"})
            logger.info(f"{member} added successfully")
        else:
            result.append({"status": "failure"})
            logger.error(f"{member} couldn't be added.")

    return jsonify(result)


@app.route("/get_members", methods=['POST'])
def get_members():
    try:
        list_members= db.read_record(twitter_id= None)
        logger.info(f'{list_members} are shown from Employee table')

    except Exception as e:
        logger.error(f"{e}")
    return json.dumps(list_members,use_decimal= True)

@app.route("/remove_member", methods = ["GET"])
def remove_member():
    data = request.get_json()
    twitter_id = data["twitter_id"]
    try:
        remove_employee = db.delete_records(twitter_id)
        logger.info(f"member with twitter id {twitter_id} removed")
    except Exception as e:
        logger.error(f"{e}")
    return jsonify({"status":"success"})




@app.route("/notify", methods=["GET"])
# @sched.scheduled_job(trigger= 'cron',minute = '*')
def notify():
    """Triggers mail with insights asked from read_name_sentiment_add_pattern"""
    sentiment_data = db.read_name_sentiment_add_pattern()
    logger.info(f"mailing sentiment data for {sentiment_data}")
    try:
        output = build_table(sentiment_data, 'blue_light')
        send_mail(output)
        logger.info("Mail sent successfully")
    except Exception as error:
        logger.error(f"{error}")

    return "Mail sent successfully."


@app.route("/get_member_sentiment", methods = ["GET"])
def get_member_sentiment():
    data = request.get_json()
    result = {"result": []}
    twitter_id = data["twitter_id"]
    employee_info = db.get_twitter_sentiment_pattern_of_employee(twitter_id,max_tweets = 15)
    for id, name, sentiment,sentiment_pattern in employee_info:
        result["result"].append({"id": id, "name": name, "sentiment": sentiment, "sentiment_pattern":sentiment_pattern})
    logger.info(f"{result} is updated for get_user_sentiment")
    return jsonify(result=result)

if __name__ == "__main__":
    logging.info('App started and is running successfully')
    app.run(debug = True)
