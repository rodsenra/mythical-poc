# -*- coding: utf-8 -*-
import json
import requests
from requests.auth import HTTPDigestAuth
import time
import sys

headers_ttl = {'Content-type': 'text/turtle'}
headers = {'Content-type': 'application/json'}


def load_json(filename):
    fp = open(filename, "r")
    return json.load(fp)


def load_string(filename):
    fp = open(filename, "r")
    return fp.read()


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

def create_review():

    ## Comments
    comment1_json = load_json('comment1_win8_instance.json')
    comment1_json['context'] = review_uid
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment1_json), headers=headers)
    comment1_uid = response.headers['Location']
    print("Comment1 instance " + comment1_uid)
    instances.append(comment1_uid)

    comment2_json = load_json('comment2_win8_instance.json')
    comment2_json['context'] = review_uid
    comment2_json['reply'] = comment1_uid
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment2_json), headers=headers)
    comment2_uid = response.headers['Location']
    print("Comment2 instance " + comment2_uid)
    instances.append(comment2_uid)

def load_instances():

    print("Load instances")
    instances = []

    ## Software
    software_dict = load_json('software_instance.json')
    response = requests.post('http://localhost:5100/data/tech/softwares', data=json.dumps(software_dict), headers=headers)
    software_uri = response.headers['Location']
    if software_uri is None:
        print("Failed to create software")
        sys.exit(0)
    print("Software instance " + software_uri)
    instances.append(software_uri)

    ## Review
    review_json = load_json('review_win8_instance.json')
    review_json['http://semantica.globo.com/tech/schemas/revises'] = software_uri
    response = requests.post('http://localhost:5100/data/tech/reviews', data=json.dumps(review_json), headers=headers)
    review_uri = response.headers['Location']
    print("Review instance " + review_uri)
    instances.append(review_uri)

    ## Comments
    comment_json = load_json('comment_1_win8_instance.json')
    comment_json['http://semantica.globo.com/tech/schemas/comments'] = review_uri
    response = requests.post('http://localhost:5100/data/tech/comments', data=json.dumps(comment_json), headers=headers)
    comment_uri = response.headers['Location']
    print("Comment instance " + comment_uri)
    instances.append(comment_uri)

    comment_json = load_json('comment_2_win8_instance.json')
    comment_json['http://semantica.globo.com/tech/schemas/comments'] = review_uri
    response = requests.post('http://localhost:5100/data/tech/comments', data=json.dumps(comment_json), headers=headers)
    comment_uri = response.headers['Location']
    print("Comment instance " + comment_uri)
    instances.append(comment_uri)

    return instances


def retrieve_data(path_name):
    response = requests.get('http://localhost:5100/data/{0}'.format(path_name), headers=headers)
    print("Retrieve {0}".format(path_name))
    print(response.json())

if __name__ == '__main__':
    wipeout_armageddon()
    load_schemas()
    paths = load_instances()
    #retrieve_data('schemas/software')
    #retrieve_data('schemas/review')
    #retrieve_data('schemas/comment')
