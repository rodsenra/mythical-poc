#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import json

import requests
import rdflib
from rdflib import Graph, plugin, OWL, URIRef, Literal
from rdflib.namespace import Namespace, NamespaceManager
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from SPARQLWrapper import SPARQLWrapper, JSON

from apiglobo.settings import *

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

TRIPLE_TEMPLATE ="%s %s %s."
INSERT_TEMPLATE = """
INSERT DATA INTO <%s> {
  %s
}
"""
RETRIEVE_TEMPLATE = """
select ?property ?value ?nested_property ?nested_value from <%s> {
  <%s> ?property ?value .
  ?s ?property ?value .
  OPTIONAL {
   ?property rdfs:range ?range_p .
   ?value a ?range_p .
   ?value ?nested_property ?nested_value .
 }
} 
"""

def create_schema(ttl, context, collection, slug=None):
    g = Graph() #namespace_manager=new_namespace_manager(context, resource_collection))
    g.parse(data=ttl, format="n3")
    final_triples = []
    for s,p,o in g:
        final_triples.append(TRIPLE_TEMPLATE % (s.n3(), p.n3(), o.n3()))
    graph = DEFAULT_GRAPH  + context + "/"
    query = INSERT_TEMPLATE % (graph, "\n".join(final_triples))
    query_results = query_sparql(query)
    # FIX: verify operation success 
    
    # OBS: URI present in TTL must adhere to the formula below. It must be validated.
    uri = "/".join((BASE_URI, context, collection, slug))
    return uri

def _encapsulate(value):
    if value.startswith('http'): # FIXME: use regexp to detect URL instead of this
        result = URIRef(value)
    else:
        result = Literal(value)
    return result

def create_instance(json_dict, context, collection, slug=None):
    slug =  slug or str(uuid.uuid4())
    uri = "/".join((BASE_URI, context, collection, slug))

    # FIXME: handle non-flat JSONS ?? Think about this!
    final_triples = []
    for p, o in json_dict.items():
       final_triples.append(TRIPLE_TEMPLATE % (_encapsulate(uri).n3(),
                                                _encapsulate(p).n3(),
                                                _encapsulate(o).n3()))
       inverse_predicates = inverse_of(p, context)
       if inverse_predicates:
           for inverse_predicate in inverse_predicates:
               final_triples.append(TRIPLE_TEMPLATE % (_encapsulate(o).n3(),
                                                       _encapsulate(inverse_predicate).n3(),
                                                       _encapsulate(uri).n3()))

    graph = DEFAULT_GRAPH  + context + "/"
    query = INSERT_TEMPLATE % (graph, "\n".join(final_triples))
    query_sparql(query)
    # FIXME: verify operation success
    return uri


def inverse_of(predicate, context):
    graph = DEFAULT_GRAPH + context + "/"

    query = """
    SELECT ?inv_prop
    FROM <%s>
    WHERE {
        <%s> owl:inverseOf ?inv_prop
    }
    """ % (graph, predicate)
    results = []
    sparql_result = query_sparql(query)
    triples = sparql_result["results"]["bindings"]
    for i in triples:
        results.append(i["inv_prop"]["value"])

    return results


def clean_up_dict(d):
    result = {}
    for key, old_container in d.items():
        if isinstance(old_container, dict):
            # transform (dict of dicts) into (list of dicts)
            new_container = []
            for k,v in old_container.items():
                v['uri'] = k  
                new_container.append(v)
            result[key] = new_container
        else:
            # there is no transformation, just copy key/value into new dict
            result[key] = old_container
            
        # simplify unitary list
        if isinstance(result[key], list) and len(result[key])==1:
            result[key] = result[key][0]

    return result

def retrieve_instance(context, collection, slug):
    uri = "/".join((BASE_URI, context, collection, slug))
    graph = DEFAULT_GRAPH + context + "/"
    query = RETRIEVE_TEMPLATE % (graph, uri)
    query_result = query_sparql(query)
    # FIX: verify operation success
    triples = query_result['results']['bindings']
    result = {}
    def create_or_append_to_list(container, key, item):
        if key in container:
            container[key].append(item)
        else:
            container[key] = [item]
    
    for row in triples:
        key = row['property']['value']
        if 'nested_property' not in row:
            result[key] = row['value']['value']
            #create_or_append_to_list(result, key, row['value']['value'])
        else:
            # I have nested properties
            if key not in result:
                result[key] = {}
            property_key = row['value']['value']
            if property_key not in result[key]:
                result[key][property_key] = {}
            nested_key =  row['nested_property']['value']
            result[key][property_key][nested_key] = row['nested_value']['value']


    return clean_up_dict(result)

# FIXME: implement transaction all-or-nothing to add data to all DBs

def update(obj, namespace, resource_type, resource_id):
    pass


def create_or_update(obj, ctx, resource_collection, slug):
    # TODO: think about sync model between backend databases, for the time being assume in sync
    # We assume that optional fields are not present in the input data (json format),
    # if this holds then we should remove non-filled fields
    refered_node = None
    create(obj, ctx, resource_collection, slug)


def delete(namespace, resource_type, resource_id):
    pass

