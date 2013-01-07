#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apiglobo.settings import ES_ENDPOINT
from pyelasticsearch import ElasticSearch

DEFAULT_NAMESPACE = "data"

es = ElasticSearch(ES_ENDPOINT)

class MythicalDBException(Exception):
    pass

def create(namespace, resource_type, obj):
    record = es.index(namespace, resource_type, obj)
    if not record['ok']:
        raise MythicalDBException("Failed to index record {0:s} in ElasticSearch.".format(obj))
    return record['_id']


def update(obj, namespace, resource_type, resource_id):
    pass


def retrieve(namespace, resource_type, resource_id):
    object_in_es = es.get(namespace, resource_type, resource_id)
    return object_in_es['_source'] 


def delete(namespace, resource_type, resource_id):
    pass
