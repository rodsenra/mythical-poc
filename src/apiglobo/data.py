# -*- coding: utf-8 -*-

from flask import Blueprint, Response, request, jsonify
import mythicaldb

data_blueprint = Blueprint('data_blueprint', __name__)

NAMESPACE = "dataservices"


@data_blueprint.route("/data/reviews/<item_id>", methods=['GET'])
def get_review(item_id):
    doc = mythicaldb.retrieve(NAMESPACE, "review", item_id)
    response = jsonify(doc)
    response.status_code = 200
    return response
