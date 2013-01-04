# -*- coding: utf-8 -*-
from flask import Blueprint, Response, request
import mythicaldb

schema_blueprint = Blueprint('schema_blueprint', __name__)

NAMESPACE = "dataservices"

@schema_blueprint.route("/schemas", methods=['POST'])
def create():
    mythicaldb.create(request.json, NAMESPACE, "schema", request.json["meta"]["schema_name"])
    response = Response(status=201)
    response.headers['Location'] = 'dummy'
    return response


@schema_blueprint.route("/schemas", methods=['GET'])
def list():
    response = Response(status=200)
    return response

@schema_blueprint.route("/schemas/<schema_id>", methods=['GET'])
def find(schema_id):
    response = Response(status=200)
    return response
