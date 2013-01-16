# -*- coding: utf-8 -*-

from flask import Blueprint, Response, request, jsonify, abort
from apiglobo.util import crossdomain
from apiglobo import mythicaldb
from apiglobo.mythicaldb import DEFAULT_NAMESPACE as NAMESPACE

data_blueprint = Blueprint('data_blueprint', __name__)

def primary_validation():
    try:
        request.json['$schema']
    except KeyError:
        abort(400)

@data_blueprint.route("/data/<type_name>", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_data(type_name):
    primary_validation()
    uid = mythicaldb.create(request.json, NAMESPACE, type_name)
    response = Response(status=201)
    response.headers['Location'] = uid
    return response


@data_blueprint.route("/data/<type_name>/<doc_slug>", methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def create_with_id(type_name, doc_slug):
    primary_validation()
    uid = mythicaldb.create_or_update(request.json, NAMESPACE, type_name, doc_slug)
    response = Response(status=201)
    response.headers['Location'] = uid
    return response


@data_blueprint.route("/data/<type_name>", methods=['GET'])
@crossdomain(origin='*')
def filter_data(type_name):
    if request.args:
        # Convention: if there are args it implies a search
        results = mythicaldb.search(request.args["q"],
                                    namespace=NAMESPACE,
                                    resource_type=type_name)
        filterd_results_by_type = [dict(item['_source'], **{'id': item['_id']}) for item in results['hits']['hits']]
        response = jsonify({"results": filterd_results_by_type})
        response.status_code = 200
        return response
    else:
        abort(404)


@data_blueprint.route("/data/<type_name>/<doc_slug>", methods=['GET'])
@crossdomain(origin='*')
def retrieve(type_name, doc_slug):
    doc = mythicaldb.retrieve(NAMESPACE, type_name, doc_slug)
    if doc is None:
        abort(404)
    response = jsonify(doc)
    response.status_code = 200
    return response


@data_blueprint.route("/data/query", methods=['GET'])
@crossdomain(origin='*')
def list_supported_query_languages():
    languages_json = {
        "cypher": "{0}{1}".format(request.url_root, "data/query/cypher"),
        "gremlin": "{0}{1}".format(request.url_root, "data/query/gremlin")
    }
    return jsonify(languages_json)


@data_blueprint.route("/data/query/cypher", methods=['GET'])
@crossdomain(origin='*')
def query_using_cypher():
    response = mythicaldb.graph_query("cypher", request.data)
    return response


@data_blueprint.route("/data/query/gremlin", methods=['GET'])
@crossdomain(origin='*')
def query_using_gremlin():
    response = mythicaldb.graph_query("gremlin", request.data)
    return jsonify(response)


@data_blueprint.route("/data", methods=['GET'])
def list():
    raise NotImplemented
