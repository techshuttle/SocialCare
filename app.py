from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_homepage():
    return jsonify({"Result": "Success"})


@app.route("/get_urls", methods=['GET'])
def get_urls():
    # call database read function to get data urls for each member in database
    result = {}
    return jsonify(result)


@app.route("/add_sentiment", methods=["POST"])
def add_sentiment():
    output = request.get_json()
    # call database update function to add sentiment
    result = {"status": 1}
    return jsonify(result)


@app.route("/add_members", methods=['POST'])
def add_members():
    data = request.get_json()
    # call database create/update function to add members
    result = {"status": 1}
    return jsonify(result)


@app.route("/get_members", methods=['POST'])
def add_members():
    data = request.get_json()
    # call database read function to send members information
    result = {"status": 1}
    return jsonify(result)


if __name__ == "__main__":
    logging.info('App started and is running successfully')
    app.run()
