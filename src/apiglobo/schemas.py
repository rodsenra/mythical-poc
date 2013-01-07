# -*- coding: utf-8 -*-
from flask import Blueprint, Response, request, jsonify
from apiglobo import mythicaldb
from apiglobo.mythicaldb import DEFAULT_NAMESPACE as NAMESPACE

schema_blueprint = Blueprint('schema_blueprint', __name__)

@schema_blueprint.route("/schemas", methods=['POST'])
def create():
    schema_id = mythicaldb.create(NAMESPACE, "schema", request.json)
    response = Response(status=201)
    response.headers['Location'] = '/schemas/{0}'.format(schema_id)
    return response


@schema_blueprint.route("/schemas", methods=['GET'])
def list():
    response = Response(status=200)
    return response

@schema_blueprint.route("/schemas/<schema_id>", methods=['GET'])
def find(schema_id):
    doc = mythicaldb.retrieve(NAMESPACE, "schema", schema_id)
    response = jsonify(doc)
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
