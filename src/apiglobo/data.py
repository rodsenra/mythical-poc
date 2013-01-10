# -*- coding: utf-8 -*-

from flask import Blueprint, Response, request, jsonify, abort
from apiglobo.util import crossdomain
from apiglobo import mythicaldb
from apiglobo.mythicaldb import DEFAULT_NAMESPACE as NAMESPACE

data_blueprint = Blueprint('data_blueprint', __name__)


@data_blueprint.route("/data/<type_name>", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_review(type_name):
    doc_id = mythicaldb.create(NAMESPACE, type_name, request.json)
    response = Response(201)
    response.headers['Location'] = '/data/{0}/{1}'.format(type_name, doc_id)
    return response


@data_blueprint.route("/data/<type_name>", methods=['GET'])
@crossdomain(origin='*')
def filter_review(type_name):
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

#    doc_id = mythicaldb.create(NAMESPACE, type_name, request.json)
#    response = Response(201)
#    response.headers['Location'] = '/data/{0}/{1}'.format(type_name, doc_id)
#    return response


@data_blueprint.route("/data/<type_name>/<item_id>", methods=['GET'])
def get_review(type_name, item_id):
    doc = mythicaldb.retrieve(NAMESPACE, type_name, item_id)
    response = jsonify(doc)
    response.status_code = 200
    return response
