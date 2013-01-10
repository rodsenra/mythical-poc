# -*- coding: utf-8 -*-
from flask import Blueprint, Response, request, jsonify
from apiglobo import mythicaldb
from apiglobo.mythicaldb import DEFAULT_NAMESPACE as NAMESPACE

schema_blueprint = Blueprint('schema_blueprint', __name__)

@schema_blueprint.route("/data", methods=['POST'])
def create():
    schema_id = mythicaldb.create(NAMESPACE, "schema", request.json)
    response = Response(status=201)
    response.headers['Location'] = '/data/{0}'.format(schema_id)
    return response

@schema_blueprint.route("/data/<schema_id>", methods=['PUT'])
def create_with_id(schema_id):
    schema_id = mythicaldb.create(NAMESPACE, "schema", request.json, schema_id)
    response = Response(status=201)
    response.headers['Location'] = '/data/{0}'.format(schema_id)
    return response

@schema_blueprint.route("/data", methods=['GET'])
def list():
    response = Response(status=200)
    return response

@schema_blueprint.route("/data/<schema_id>", methods=['GET'])
def find(schema_id):
    doc = mythicaldb.retrieve(NAMESPACE, "schema", schema_id)
    response = jsonify(doc)
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
