#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import json

import requests
import rdflib
from rdflib import Graph, plugin, OWL
from rdflib.namespace import Namespace, NamespaceManager
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from SPARQLWrapper import SPARQLWrapper, JSON

from apiglobo.settings import *

BASE_URL = 'http://semantica.globo.com'

DEFAULT_NAMESPACE = "data"

JSON_SCHEMA_URI = "http://json-schema.org/schema"
SCHEMAS_INDEX = 'schemas'

sparql_db = SPARQLWrapper(SPARQL_ENDPOINT_AUTH)
sparql_db.setCredentials(SPARQL_ENDPOINT_USER,
                         SPARQL_ENDPOINT_PASSWORD,
                         SPARQL_ENDPOINT_AUTH_MODE,
                         SPARQL_ENDPOINT_REALM)

def query_sparql(query):
    sparql_db.setQuery(query)
    sparql_db.setReturnFormat(JSON)
    results = sparql_db.query().convert()
    return results

class MythicalDBException(Exception):
    pass

TRIPLE_TEMPLATE ="<%s> <%s> <%s>."
INSERT_TEMPLATE = """
INSERT DATA INTO <%s> {
  %s
}
"""

def create(ttl, context, resource_collection, slug=None):
    g = Graph() #namespace_manager=new_namespace_manager(context, resource_collection))
    g.parse(data=ttl, format="n3")
    final_triples = []
    for s,p,o in g:
        final_triples.append(TRIPLE_TEMPLATE % (s,p, o))
    query = INSERT_TEMPLATE % (DEFAULT_GRAPH, "\n".join(final_triples))
    results = query_sparql(query)
    
    # inject slug into object
    # slug = obj["slug"] = slug or str(uuid.uuid4())

    # inject id into object with a common field name
    # uid = obj["uid"] = "/".join(("", namespace, resource_type, slug))

    
    
    # FIXME: implement transaction all-or-nothing to add data to all DBs
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


def create_or_update(obj, ctx, resource_collection, slug):
    # TODO: think about sync model between backend databases, for the time being assume in sync
    # We assume that optional fields are not present in the input data (json format),
    # if this holds then we should remove non-filled fields
    refered_node = None
    # FIXME: map the ctx concept to Neo4J
    #ref_index = graph_db.get_index(neo4j.Node, resource_collection)
    
#    if ref_index:
#        refered_node = ref_index.get("slug", slug)
#    
#    if refered_node:
#        update(obj, ctx, resource_collection, slug)
#    else:
    create(obj, ctx, resource_collection, slug)


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
