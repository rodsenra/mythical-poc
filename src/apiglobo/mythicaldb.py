#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apiglobo.settings import ES_ENDPOINT
from pyelasticsearch import ElasticSearch

es = ElasticSearch(ES_ENDPOINT)


def create(obj, namespace, resource_type, resource_id=None):
    pass


def update(obj, namespace, resource_type, resource_id):
    pass


def retrieve(namespace, resource_type, resource_id):
    obj = None
    return obj


def delete(namespace, resource_type, resource_id):
    pass
