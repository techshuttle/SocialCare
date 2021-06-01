import logging
import logging.config
import os
import smtplib
import psycopg2
import psycopg2.extras
import config
import simplejson as json

from flask import Flask, request, jsonify
from src import twitter_utils
from src import db_utils as db
from src.send_email import send_mail
from pretty_html_table import build_table
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(daemon =True)
sched.start()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(lineno)d: %(levelname)s :%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# from src.logger import setup_logger
# alog = setup_logger("app_logger", "./logs/app_logfile.log")


app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_homepage():
    return jsonify({"Result": "Success"})
    logger.info("homepage successful")

@app.route("/get_urls", methods=['GET'])
def get_urls():
    # data = request.get_json()
    # print(data)
    # for member in data:
    #     twitter_id = member["twitter_id"]
    # logger.info(f"{data} is our data for get_urls")
    result = {"result": []}
    list_urls = db.get_url(twitter_id = None)
    for id, twitter,linkedin in list_urls:
        result["result"].append({"id": id, "linkedin": linkedin, "twitter": twitter})
    logger.info("urls read successfully")
    return jsonify(result=result)


@app.route("/add_sentiment", methods=[ "POST"])
def add_sentiment():
    list_sentiments = db.update_tweet_sentiment_from_ids()
    logger.info(f"status of sentiments {list_sentiments}")
    if list_sentiments[0] == 1:
        result = {"status": "success"}
    else:
        result = {"status": "failure"}
    logger.info("Added Sentiments successfully")
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
    # return jsonify(list_members)


# @app.route("/notify", methods=["GET"])
@sched.scheduled_job(trigger= 'cron',day = '*')
def notify():
    sentiment_data = db.read_name_sentiment()
    logger.info(f"mailing sentiment data for {sentiment_data}")
    try:
        output = build_table(sentiment_data, 'blue_light')
        send_mail(output)
        logger.info("Mail sent successfully")
    except Exception as error:
        logger.error(f"{error}")

    return "Mail sent successfully."

if __name__ == "__main__":
    logging.info('App started and is running successfully')
    app.run(debug = True)
