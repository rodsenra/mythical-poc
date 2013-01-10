#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import json
from py2neo import neo4j
from pyelasticsearch import ElasticSearch
from apiglobo.settings import ES_ENDPOINT, NEO4J_ENDPOINT

DEFAULT_NAMESPACE = "data"

txt_search_db = ElasticSearch(ES_ENDPOINT)
graph_db = neo4j.GraphDatabaseService(NEO4J_ENDPOINT)


class MythicalDBException(Exception):
    pass


def create(namespace, resource_type, obj, uid=None):
    uid = uid if uid  else uuid.uuid4()  
    obj["uid"] = str(uid) # inject id into object with a common field name
    # FIXME: implement transaction all-or-nothing to add data to all DBs

    record = txt_search_db.index(namespace, resource_type, obj, id=uid)
    if not record['ok']:
        raise MythicalDBException("Failed to index record {0:s} in ElasticSearch.".format(obj))
    
    # Neo4J does not accept nested properties
    # We have chosen to embed the data structure as a json string instead
    node_record = dict([(key, json.dumps(value)) for key, value in obj.items()])
    # FIXME ids Neo4J - ES
    node_list = graph_db.create(node_record)
    print(node_list[0].id)
    return record['_id']


def update(obj, namespace, resource_type, resource_id):
    pass


def retrieve(namespace, resource_type, resource_id):
    object_in_es = txt_search_db.get(namespace, resource_type, resource_id)
    return object_in_es['_source'] 


def delete(namespace, resource_type, resource_id):
    pass


def search(text, namespace=None, resource_type=None):
    return txt_search_db.search(text, doc_type=resource_type, index=namespace)
