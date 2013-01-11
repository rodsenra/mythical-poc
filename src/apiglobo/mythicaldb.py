#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import json
from py2neo import neo4j
from pyelasticsearch import ElasticSearch
from apiglobo import settings

DEFAULT_NAMESPACE = "data"

JSON_SCHEMA_URI = "http://json-schema.org/schema"
SCHEMAS_INDEX = 'schemas'

txt_search_db = ElasticSearch(settings.ES_ENDPOINT)
graph_db = neo4j.GraphDatabaseService(settings.NEO4J_ENDPOINT)


class MythicalDBException(Exception):
    pass

def get_references(obj):
    refs = []
    for key,subprop_dict in obj.get("properties", {}).items():
        for subprop_key,value in subprop_dict.items():
            if subprop_key=="$ref":
                relationship_name = subprop_dict.get("relationship_name","relates")
                refs.append((relationship_name, value))
    return refs


def create(obj, namespace, resource_type, slug=None):

    # inject slug into object
    slug = obj["slug"] = slug or str(uuid.uuid4())
    
    # inject id into object with a common field name
    uid = obj["uid"] = "/".join(("", namespace, resource_type, slug)) 
    
    # FIXME: implement transaction all-or-nothing to add data to all DBs

    # id inside elasticsearch is sufficient to be a slug because it will keep path (considering the ES index)
    record = txt_search_db.index(namespace, resource_type, obj, id=slug)
    if not record['ok']:
        raise MythicalDBException("Failed to index record {0:s} in ElasticSearch.".format(obj))
    
    # Neo4J does not accept nested properties
    # We have chosen to embed the data structure as a json string instead
    node_record = dict([(key, json.dumps(value)) for key, value in obj.items()])
    # FIXME ids Neo4J - ES
    node_list = graph_db.create(node_record)
    pivot_node = node_list[0]

    index = graph_db.get_or_create_index(neo4j.Node, resource_type)
    index.add("slug", slug, pivot_node)
    
    refs = get_references(obj)
    for relationship_name, node_path in refs:
        path_fragments = node_path.split("/")
        ref_type = path_fragments[-2]
        ref_slug = path_fragments[-1]
        ref_index = graph_db.get_index(neo4j.Node, ref_type)
        referred_nodes = ref_index.get("slug", ref_slug)
        for referred_node in referred_nodes: 
            pivot_node.create_relationship_to(referred_node, relationship_name)

    # Detect if it is a schema or instance
    schema_uid = obj['$schema']
    if (schema_uid != JSON_SCHEMA_URI) and (resource_type != SCHEMAS_INDEX):
        uid_fragments = schema_uid.split("/")
        schema_slug = uid_fragments[-1]
        schemas_index = graph_db.get_index(neo4j.Node, SCHEMAS_INDEX)
        schema_nodes = schemas_index.get("slug", schema_slug)
        for schema_node in schema_nodes:
            # highlander - there should be only one!
            pivot_node.create_relationship_to(schema_node, 'describedby')

        # ----- Search by ES 
#        search_response = txt_search_db.search("uid:{0}".format(schema_uid), SCHEMAS_INDEX)     
#        if search_response[u'hits'][u'total']!=1:
#            raise Exception("Inconsistency in Database. More than one schema defined for {0}".format(schema_uid))
#        schema_doc = search_response[u'hits'][u'hits'][0]['_source']
#        schema_doc['']

    return uid


def update(obj, namespace, resource_type, resource_id):
    pass


def create_or_update(obj, namespace, resource_type, resource_id):
    # TODO: think about sync model between backend databases, for the time being assume in sync
    refered_node = None
    ref_index = graph_db.get_index(neo4j.Node, resource_type)
    
    if ref_index:
        refered_node = ref_index.get("slug", resource_id)
    
    if refered_node:
        update(obj, namespace, resource_type, resource_id )
    else:
        create(obj, namespace, resource_type, resource_id)

def retrieve(namespace, resource_type, resource_id):
    object_in_es = txt_search_db.get(namespace, resource_type, resource_id)
    return object_in_es['_source'] 


def delete(namespace, resource_type, resource_id):
    pass


def search(text, namespace=None, resource_type=None):
    return txt_search_db.search(text, doc_type=resource_type, index=namespace)
