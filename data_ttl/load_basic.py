# -*- coding: utf-8 -*-
import json
import requests
from requests.auth import HTTPDigestAuth
import time
import sys
from pprint import pprint

headers_ttl = {'Content-type': 'text/turtle'}
headers = {'Content-type': 'application/json'}


def load_json(filename):
    fp = open(filename, "r")
    return json.load(fp)


def load_string(filename):
    fp = open(filename, "r")
    return fp.read()

def print_or_abort(status, uri):
    print("Response {0} {1}".format(status, uri))
    if (status not in (200,201)) or (uri is None):
        sys.exit(0)

def wipeout_armageddon():
    print("Clean up databases")
    response = requests.get('http://localhost:8890/sparql-auth?default-graph-uri=&query=%0D%0Aclear+graph+%3Chttp%3A%2F%2Fmythical_poc.globo.com%2Ftech%2F%3E&should-sponge=&format=text%2Fhtml&timeout=0&debug=on',
                             auth=HTTPDigestAuth('api-semantica', 'api-semantica'))  
    print(response)

def load_schemas():
    print("Load schemas")
    requests.put('http://localhost:5100/data/tech/schemas/SoftwareCategory', data=load_string('software_category.ttl'), headers=headers_ttl)
    requests.put('http://localhost:5100/data/tech/schemas/Software', data=load_string('software.ttl'), headers=headers_ttl)
    requests.put('http://localhost:5100/data/tech/schemas/Comment', data=load_string('comment.ttl'), headers=headers_ttl)
    requests.put('http://localhost:5100/data/tech/schemas/Review', data=load_string('review.ttl'), headers=headers_ttl)

def load_instances():

    print("Load instances")
    instances = []

    ## Software
    software_dict = load_json('software_instance.json')
    response = requests.post('http://localhost:5100/data/tech/softwares', data=json.dumps(software_dict), headers=headers)
    software_uri = response.headers['Location']
    print_or_abort(response.status_code, software_uri) 
    instances.append(software_uri)

    ## Review
    review_json = load_json('review_win8_instance.json')
    review_json['http://semantica.globo.com/tech/schemas/revises'] = software_uri
    response = requests.post('http://localhost:5100/data/tech/reviews', data=json.dumps(review_json), headers=headers)
    review_uri = response.headers['Location']
    print_or_abort(response.status_code, review_uri)
    instances.append(review_uri)

    ## Comments
    comment_json = load_json('comment_1_win8_instance.json')
    comment_json['http://semantica.globo.com/tech/schemas/comments'] = review_uri
    response = requests.post('http://localhost:5100/data/tech/comments', data=json.dumps(comment_json), headers=headers)
    comment1_uri = response.headers['Location']
    print_or_abort(response.status_code, comment1_uri)
    instances.append(comment1_uri)

    comment_json = load_json('comment_2_win8_instance.json')
    comment_json['http://semantica.globo.com/tech/schemas/comments'] = review_uri
    comment_json['http://semantica.globo.com/tech/schemas/replies'] = comment1_uri
    response = requests.post('http://localhost:5100/data/tech/comments', data=json.dumps(comment_json), headers=headers)
    comment2_uri = response.headers['Location']
    print_or_abort(response.status_code, comment2_uri)
    instances.append(comment2_uri)

    return instances


def retrieve_data(instances):
    api_uris = [i.replace("http://semantica.globo.com/","http://localhost:5100/data/") for i in instances]
    for uri in api_uris:
        response = requests.get(uri, headers=headers)
        print("\n\nRetrieve {0}".format(uri))
        pprint(response.json)

if __name__ == '__main__':
    wipeout_armageddon()
    load_schemas()
    paths = load_instances()
    retrieve_data(paths)
