#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import json
import py2neo
import requests
from py2neo import neo4j, cypher, gremlin
from pyelasticsearch import ElasticSearch
from SPARQLWrapper import SPARQLWrapper

from apiglobo import settings

DEFAULT_NAMESPACE = "data"

JSON_SCHEMA_URI = "http://json-schema.org/schema"
SCHEMAS_INDEX = 'schemas'

txt_search_db = ElasticSearch(settings.ES_ENDPOINT)
graph_db = neo4j.GraphDatabaseService(settings.NEO4J_ENDPOINT)
sparql_db = SPARQLWrapper(settings.SPARQL_ENDPOINT_AUTH)

class MythicalDBException(Exception):
    pass

def split_uid(uid):
    fragments = uid.split("/")
    _namespace = fragments[-3]
    _type = fragments[-2]
    _slug = fragments[-1]
    return (_namespace, _type, _slug)


def unmarshal_node(node_dict):
    "Return dictionary with json strings expanded"
    result = {}
    for key,value in node_dict.items():
        effective_value = value
        if isinstance(value, basestring):
            try:
                effective_value = json.loads(value)                    
            except ValueError:
                pass
        result[key] = effective_value
    return result


def get_references_from_input_json(obj):
    refs = []
    for key,subprop_dict in obj.items():
        for subprop_key,value in subprop_dict.items():
            if subprop_key=="$ref":
                relationship_name = subprop_dict.get("relationship_name","relates")
                refs.append((key, relationship_name, value))
    return refs

def get_references_from_graph(node):
    # (key, relationship_name, value))
    pass

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
    txt_search_db.refresh(namespace)
    
    # Neo4J does not accept nested properties
    # We have chosen to embed the data structure as a json string instead
    node_record = {}
    for key, value in obj.items():
        if type(value) in (dict,list,tuple):
            node_record[key] = json.dumps(value)
        else:
            node_record[key] = value

    # FIXME ids Neo4J - ES
    node_list = graph_db.create(node_record)
    pivot_node = node_list[0]

    index = graph_db.get_or_create_index(neo4j.Node, resource_type)
    index.add("slug", slug, pivot_node)

    # Detect if it is a schema or instance
    schema_uid = obj['$schema']

    if (schema_uid == JSON_SCHEMA_URI) and (resource_type == SCHEMAS_INDEX):
        # The input data is a schema
        refs = get_references_from_input_json(obj.get("properties", {}))
        for property_name, relationship_name, node_path in refs:
            values = split_uid(node_path)
            ref_ns, ref_type, ref_slug = values
            ref_index = graph_db.get_index(neo4j.Node, ref_type)
            referred_nodes = ref_index.get("slug", ref_slug)
            for referred_node in referred_nodes: 
                pivot_node.create_relationship_to(referred_node, relationship_name)
    else:
        # The input data is an instance
        
        # Create relation between instance and its schema
        uid_fragments = schema_uid.split("/")
        schema_slug = uid_fragments[-1]
        schemas_index = graph_db.get_index(neo4j.Node, SCHEMAS_INDEX)
        schema_nodes = schemas_index.get("slug", schema_slug)
        schema_node = schema_nodes[0]  # highlander - there should be only one!
        edge_schema = pivot_node.create_relationship_to(schema_node, 'describedby')
            
        # Create relation between instance and referred instances
        # There is a premise here that the only schema type will be JSON_SCHEMA_URI
        # if that changes then this code should consider this alternate case
        search_response = txt_search_db.search('uid:"{0}"'.format(schema_uid), 
                                               doc_type=SCHEMAS_INDEX,
                                               index=namespace)
        if search_response[u'hits'][u'total']!=1:
            raise Exception("Inconsistency in Database. More than one schema defined for {0}".format(schema_uid))

        schema_obj = search_response[u'hits'][u'hits'][0]['_source']
        obj_refs = get_references_from_input_json(schema_obj.get("properties", {}))
        for property_name, relationship_name, node_path in obj_refs:
            property_value = obj.get(property_name)
            if property_value:
                ref_ns, ref_type, ref_slug = split_uid(property_value)
                referred_index = graph_db.get_index(neo4j.Node, ref_type)
                referred_nodes = referred_index.get("slug", ref_slug)
                if referred_nodes:
                    referred_node = referred_nodes[0]  # highlander - there should be only one!
                    referred_node_id = obj[property_name]
                    pivot_node.create_relationship_to(referred_node, relationship_name)

    return uid


def retrieve(namespace, resource_type, resource_id):
    # Obtain instance from type + slug
    instance_index = graph_db.get_index(neo4j.Node, resource_type)
    instance_nodes = instance_index.get("slug", resource_id)
    if not instance_nodes:
        return None
    
    # FIXME: generate error if more than one instance is found
    instance_node = instance_nodes[0]
    instance_obj = unmarshal_node(instance_node.get_properties())
    
    if instance_obj.get('$schema') != JSON_SCHEMA_URI:
        # Obtain schema from given instance
        # FIXME: generate error if more than one schema is retrieved from describedby

        relations = instance_node.get_relationships()
        for relation in relations:
            if relation.type=='describedby':
                continue
            values = []
            for related_node in relation.nodes:
                if related_node == instance_node:
                    continue
                values.append(unmarshal_node(related_node.get_properties()))
            if len(values)==1:
                instance_obj[relation.type] = values[0]
            else:
                instance_obj[relation.type] = values
        
#        schema_node = instance_node.get_related_nodes(0,"describedby")[0]
#        prop_str = schema_node.get_properties()["properties"]
#        schema_properties = json.loads(prop_str)
#        refs = get_references_from_input_json(schema_properties)
#        for key, relationship_name, value in refs:
#            related_nodes = instance_node.get_related_nodes(0, relationship_name)
#            values = []
#            for related_node in related_nodes:
#                values.append(unmarshal_node(related_node.get_properties()))
#            if len(values)==1:
#                instance_obj[key] = values[0]
#            else:
#                instance_obj[key] = values
        
    return instance_obj

    #object_in_es = txt_search_db.get(namespace, resource_type, resource_id)
    #return object_in_es['_source']


def update(obj, namespace, resource_type, resource_id):
    pass


def create_or_update(obj, namespace, resource_type, resource_id):
    # TODO: think about sync model between backend databases, for the time being assume in sync
    # We assume that optional fields are not present in the input data (json format),
    # if this holds then we should remove non-filled fields
    refered_node = None
    ref_index = graph_db.get_index(neo4j.Node, resource_type)
    
    if ref_index:
        refered_node = ref_index.get("slug", resource_id)
    
    if refered_node:
        update(obj, namespace, resource_type, resource_id )
    else:
        create(obj, namespace, resource_type, resource_id)


def delete(namespace, resource_type, resource_id):
    pass


def search(text, namespace=None, resource_type=None):
    return txt_search_db.search(text, doc_type=resource_type, index=namespace)


def graph_query(language, data_payload):
    if language == "cypher":
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:7474/db/data/cypher', data=data_payload, headers=headers)
        return response.text
    elif language == "gremlin":
        response = gremlin.execute(data_payload, graph_db)
        return {"response" : response}
