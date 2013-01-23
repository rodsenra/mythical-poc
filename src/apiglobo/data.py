# -*- coding: utf-8 -*-

from flask import Blueprint, Response, request, jsonify, abort
from apiglobo.util import crossdomain
from apiglobo import mythicaldb
from apiglobo.mythicaldb import DEFAULT_NAMESPACE as NAMESPACE

data_blueprint = Blueprint('data_blueprint', __name__)

def primary_validation():
    pass

@data_blueprint.route("/data", methods=['GET'])
def list():
    # list all contexts and operations
    raise NotImplemented

@data_blueprint.route("/data/<ctx>/schemas", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_schema(ctx):
    pass

@data_blueprint.route("/data/<ctx>/schemas/<slug>", methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def create_schema_with_slug(ctx, slug):
    primary_validation()
    uid = mythicaldb.create_schema(request.data, ctx, "schemas", slug)
    response = Response(status=201)
    response.headers['Location'] = uid
    return response

@data_blueprint.route("/data/<ctx>/schemas", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def list_schemas(ctx):
    pass

@data_blueprint.route("/data/<ctx>/schemas/<slug>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def retrieve_schema(ctx, slug):
    pass

@data_blueprint.route("/data/<ctx>/<collection>", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_instance(ctx, collection):
    pass

@data_blueprint.route("/data/<ctx>/<collection>/<slug>", methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def create_instance_with_slug(ctx, collection, slug):
    pass

@data_blueprint.route("/data/<ctx>/<collection>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def list_instances(ctx, collection):
    pass

@data_blueprint.route("/data/<ctx>/<collection>/<slug>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def retrieve_instance(ctx, collection, slug):
    pass


@data_blueprint.route("/data/query", methods=['GET'])
@crossdomain(origin='*')
def list_supported_query_languages():
    languages_json = {
    }
    return jsonify(languages_json)




#    primary_validation()
#    uid = mythicaldb.create(request.data, NAMESPACE, type_name)
#    response = Response(status=201)
#    response.headers['Location'] = uid
#    return response

#    primary_validation()
#    uid = mythicaldb.create_or_update(request.data, ctx, resource_collection, slug)
#    response = Response(status=201)
#    response.headers['Location'] = uid
#    return response


