# -*- coding: utf-8 -*-

from flask import Blueprint, Response, request, jsonify
import mythicaldb

data_blueprint = Blueprint('data_blueprint', __name__)

NAMESPACE = "data"

@data_blueprint.route("/data/reviews", methods=['POST'])
def create_review():
    doc_id = mythicaldb.create(NAMESPACE, "review", request.json)
    response = Response(201)
    response.headers['Location'] = '/data/reviews/{0}'.format(doc_id)
    return response

@data_blueprint.route("/data/reviews/<item_id>", methods=['GET'])
def get_review(item_id):
    doc = mythicaldb.retrieve(NAMESPACE, "review", item_id)
    response = jsonify(doc)
    response.status_code = 200
    return response
