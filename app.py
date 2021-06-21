import logging.config
from flasgger import Swagger, swag_from

from flask import Flask, request, jsonify, render_template

from src import twitter_utils
from src import db_utils as db
from src.send_email import send_mail
from pretty_html_table import build_table
from apscheduler.schedulers.background import BackgroundScheduler

from src.dashboard import create_dash_application


#Scheduler
sched = BackgroundScheduler(daemon=True)
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
swagger = Swagger(app)

create_dash_application(app)


@app.route("/", methods=['GET'])
def get_homepage():
    logger.info("homepage successful")
    return render_template("webpage_garage.html",
                           filename="static/work_from_home.jpg", organization="static/organization.jpg",
                           logo="static/logo.jpg", techshuttle="static/Spaceship.jpg"
                           )


@app.route("/add_members", methods=['POST'])
@swag_from('api_desc/add_members.yml')
def add_members():
    data = request.get_json()
    result = []
    for member in data:
        id = member["id"]
        name = member["name"]
        twitter_id = member["twitter_id"]
        # call database create/update function to add members
        add_member = db.insert_data(id, name, twitter_id)
        if add_member == 1:
            result.append({"status": "success"})
            logger.info(f"{member} added successfully")
        else:
            result.append({"status": "failure"})
            logger.error(f"{member} couldn't be added.")
    return jsonify(result)


@app.route("/get_urls", methods=['GET'])
@swag_from('api_desc/get_urls.yml')
def get_urls():
    result = {"result": []}
    list_urls = db.get_url_info()
    for twitter_id,tweet in list_urls:
        result["result"].append({"twitter_id": twitter_id,"tweet":tweet})
    logger.info(f"{result} is updated for get_urls")
    return jsonify(result=result)


@app.route("/get_members", methods=['GET'])
def get_members():
    try:
        list_members = db.read_records()
        logger.info(f'{list_members} are shown from Employee table')
    except Exception as e:
        logger.error(f"{e}")
    # return json.dumps(list_members,use_decimal= True)
    return "success"


@app.route("/add_tweet", methods=[ "GET"])
def add_tweet():
    list_tweet = db.update_tweet_from_ids()
    logger.info(f"status of sentiments {list_tweet}")
    if list_tweet[0] == 1:
        result = {"status": "success"}
        logger.info("added sentiment successfully")
    else:
        result = {"status": "failure"}
        logger.info("failed to add sentiments")
    return jsonify(result)


@app.route("/tweet_analytics", methods = ["GET"])
def add_tweet_analytics():
    list_sentiment_rcsa = db.tweet_analytics()
    logger.info(f"status of sentiments {list_sentiment_rcsa}")
    if list_sentiment_rcsa == 1:
        result = {"status": "success"}
        logger.info("added sentiment and RCSA")
    else:
        result = {"status": "failure"}
        logger.info("failed to add sentiments or RCSA")
    return jsonify(result)

@app.route("/add_sentiment_pattern", methods=["GET"])
@swag_from('api_desc/add_sentiment_pattern.yml')
def add_sentiment_pattern():
    list_pattern = db.update_twitter_sentiment_pattern_from_ids()
    logger.info(f"{add_sentiment_pattern} is working")
    if list_pattern[0] == 1:
        result = {"status": "success"}
        logger.info("added sentiment pattern successfully")
    else:
        result = {"status": "failure"}
        logger.info("failed to add sentiment pattern")
    return jsonify(result)


@app.route("/update_database_to_df", methods = ["GET"])
def update_database_to_df():
    update = db.read_data_to_dataframe()
    if update.shape[1] == 7:
        return jsonify({"result":"success"})
    else:
        return jsonify({"result":"DataFrame not updated"})


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

    return render_template("Notification.html", filename='static/Golden_Gate.png')


@app.route("/remove_member", methods = ["GET"])
def remove_member():
    data = request.get_json()
    twitter_id = data["twitter_id"]
    try:
        remove_employee = db.delete_records(twitter_id)
        logger.info(f"member with twitter id {twitter_id} removed")
    except Exception as e:
        logger.error(f"{e}")
    return jsonify({"status": "success"})


if __name__ == "__main__":
    logging.info('App started and is running successfully')
    app.run(debug=True)
