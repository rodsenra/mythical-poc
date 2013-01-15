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


def load():
    # Load schemas
    print("Load schemas")
    requests.put('http://localhost:5100/data/schemas/software', data=load_string('software_schema.json'), headers=headers)
    requests.put('http://localhost:5100/data/schemas/review', data=load_string('review_schema.json'), headers=headers)
    requests.put('http://localhost:5100/data/schemas/comment', data=load_string('comment_schema.json'), headers=headers)

    # Load instances

    ## Software
    print("Load instances")
    response = requests.post('http://localhost:5100/data/softwares', data=load_string('software_instance.json'), headers=headers)
    software_uid = response.headers['Location']
    print("Software instance " + software_uid)
    ## Review
    review_json = load_json('review_win8_instance.json')
    review_json['software'] = software_uid
    response = requests.post('http://localhost:5100/data/reviews', data=json.dumps(review_json), headers=headers)
    review_uid = response.headers['Location']
    print("Review instance " + review_uid)

    ## Comments
    comment1_json = load_json('comment1_win8_instance.json')
    comment1_json['review'] = review_uid
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment1_json), headers=headers)
    comment1_uid = response.headers['Location']
    print("Comment1 instance " + comment1_uid)

    comment2_json = load_json('comment2_win8_instance.json')
    comment2_json['review'] = review_uid
    comment2_json['reply'] = comment1_uid
    response = requests.post('http://localhost:5100/data/comments', data=json.dumps(comment2_json), headers=headers)
    comment2_uid = response.headers['Location']
    print("Comment2 instance " + comment2_uid)


if __name__ == '__main__':
    wipeout_armageddon()
    load()
