from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dynamo import Dynamo
from config import config
from loggers import logger

db = Dynamo(config.default_region, config.click_bags_table, config.click_users_table)

app = Flask(__name__)
CORS(app)

bad_request = {"message": "bad_request"}
internal_error = {"message": "internal_error"}


@app.route("/click", methods=["GET"])
def click():
    try:
        country_clicks = db.get_all_country_clicks()
        return make_response(jsonify({"message": "ok", "items": country_clicks})), 200
    except Exception as e:
        return make_response(jsonify(internal_error)), 500


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    if db:
        return make_response(jsonify({"message": "ok"})), 200
    else:
        return make_response(jsonify(internal_error)), 500
