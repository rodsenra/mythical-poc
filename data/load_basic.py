# -*- coding: utf-8 -*-
import json
import requests
import time


headers = {'Content-type': 'application/json'}


def load_json(filename):
    fp = open(filename, "r")
    return json.load(fp)


def load_string(filename):
    fp = open(filename, "r")
    return fp.read()


def wipeout_armageddon():
    print("Clean up databases")
    requests.post('http://localhost:7474/db/data/cypher', data='{"query": "start no=relationship(*) delete no"}', headers=headers)
    requests.post('http://localhost:7474/db/data/cypher', data='{"query": "start no=node(*) delete no"}', headers=headers)
    requests.delete('http://localhost:9200/data')

def load_schemas():
    print("Load schemas")
    requests.put('http://localhost:5100/data/schemas/software', data=load_string('software_schema.json'), headers=headers)
    requests.put('http://localhost:5100/data/schemas/software_category', data=load_string('software_category_schema.json'), headers=headers)
    requests.put('http://localhost:5100/data/schemas/comment', data=load_string('comment_schema.json'), headers=headers)
    requests.put('http://localhost:5100/data/schemas/review', data=load_string('review_schema.json'), headers=headers)

def create_review():
    ## Review
    review_json = load_json('review_win8_instance.json')
    review_json['software'] = software_uid
    response = requests.post('http://localhost:5100/data/reviews', data=json.dumps(review_json), headers=headers)
    review_uid = response.headers['Location']
    print("Review instance " + review_uid)
    instances.append(review_uid)

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

    ## Software Categories
    sample_category = {'$schema':'/data/schemas/software_category', 'name':'', 'items':[]}
    for category_name, slug in [(u'S.O.', 'SO'),
                          (u'Utilitátio', 'Utility'),
                          (u'Produtividade', 'Productivity'),
                          (u'Audio/Video', 'AudioVideo'),
                          (u'Internet', 'Intenet'),
                          (u'Segurança', 'Security')]:
        sample_category['name'] = category_name
        response = requests.put('http://localhost:5100/data/software_categories/{0}'.format(slug),
                                data=json.dumps(sample_category), headers=headers)
        software_category_uid = response.headers['Location']
        print("Software category instance " + software_category_uid)
        instances.append(software_category_uid)
    
    ## Software
    software_dict = load_json('software_instance.json')
    response = requests.post('http://localhost:5100/data/softwares', data=json.dumps(software_dict), headers=headers)
    software_uid = response.headers['Location']
    print("Software instance " + software_uid)
    instances.append(software_uid)


    create_review()
    
    return instances


def retrieve_data(path_name):
    response = requests.get('http://localhost:5100/data/{0}'.format(path_name), headers=headers)
    print("Retrieve {0}".format(path_name))
    print(response.json())

if __name__ == '__main__':
    wipeout_armageddon()
    load_schemas()
    paths = load_instances()
    retrieve_data('schemas/software')
    retrieve_data('schemas/review')
    retrieve_data('schemas/comment')
