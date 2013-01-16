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


def load_instances():

    print("Load instances")
    instances = []

    ## Software Categories
    sample_category = {'$schema':'/data/schemas/software_category', 'name':'', 'items':[]}
    for category_name, slug in [(u'S.O.', 'SO'),
                          (u'Utilitátio', 'Utility'),
                          (u'Produtividade', 'Productivity'),
                          (u'Audio/Video', 'AudioVideo'),
                          (u'Internet', 'Internet'),
                          (u'Segurança', 'Security')]:
        sample_category['name'] = category_name
        response = requests.put('http://localhost:5100/data/software_categories/{0}'.format(slug),
                                data=json.dumps(sample_category), headers=headers)
        software_category_uid = '/data/software_categories/{0}'.format(slug)
        print("Software category instance " + software_category_uid)
        instances.append(software_category_uid)
    
    ## Softwares
    software_dict = load_json('software_instance.json')

    response = requests.post('http://localhost:5100/data/softwares', data=json.dumps(software_dict), headers=headers)
    software_uid = response.headers['Location']
    print("Software instance " + software_uid)
    instances.append(software_uid)

    software_dict['name'] = 'Linux'    
    response = requests.post('http://localhost:5100/data/softwares', data=json.dumps(software_dict), headers=headers)
    software_uid_linux = response.headers['Location']
    print("Software instance " + software_uid_linux)
    instances.append(software_uid_linux)

    software_dict['name'] = 'WSO2'
    software_dict['category'] = '/data/software_categories/Internet'
    response = requests.post('http://localhost:5100/data/softwares', data=json.dumps(software_dict), headers=headers)
    software_uid_wso2 = response.headers['Location']
    print("Software instance " + software_uid_wso2)
    instances.append(software_uid_wso2)

    ## Review Win8
    review_json = load_json('review_win8_instance.json')
    review_json['software'] = software_uid
    response = requests.post('http://localhost:5100/data/reviews', data=json.dumps(review_json), headers=headers)
    review_uid_win8 = response.headers['Location']
    print("Review instance " + review_uid_win8)
    instances.append(review_uid_win8)

    ## Review Linux
    review_json['software'] = software_uid_linux
    review_json['title'] = 'About Linux'
    response = requests.post('http://localhost:5100/data/reviews', data=json.dumps(review_json), headers=headers)
    review_uid_linux = response.headers['Location']
    print("Review instance " + review_uid_linux)
    instances.append(review_uid_linux)

    ## Review WSO2
    review_json['software'] = software_uid_wso2
    review_json['title'] = 'WSO2: yes or no?'
    response = requests.post('http://localhost:5100/data/reviews', data=json.dumps(review_json), headers=headers)
    review_uid_wso2 = response.headers['Location']
    print("Review instance " + review_uid_wso2)
    instances.append(review_uid_wso2)

    ## Comments
    comment1_json = load_json('comment1_win8_instance.json')
    comment1_json['context'] = review_uid_win8
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment1_json), headers=headers)
    comment1_uid = response.headers['Location']
    print("Comment1 instance " + comment1_uid)
    instances.append(comment1_uid)

    comment2_json = load_json('comment2_win8_instance.json')
    comment2_json['context'] = review_uid_win8
    comment2_json['reply'] = comment1_uid
    comment2_json['body'] = 'Oi tudo bem?'
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment2_json), headers=headers)
    comment2_uid = response.headers['Location']
    print("Comment2 instance " + comment2_uid)
    instances.append(comment2_uid)

    comment2_json = load_json('comment2_win8_instance.json')
    comment2_json['context'] = review_uid_win8
    comment2_json['reply'] = comment2_uid
    comment2_json['body'] = 'Belex'
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment2_json), headers=headers)
    comment2_uid = response.headers['Location']
    print("Comment2 instance " + comment2_uid)
    instances.append(comment2_uid)

    comment2_json['context'] = review_uid_linux
    comment2_json['body'] = 'Linux rulz!'
    del comment2_json['reply'] 
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment2_json), headers=headers)
    comment2_uid = response.headers['Location']
    print("Comment3 instance " + comment2_uid)
    instances.append(comment2_uid)

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
