import unittest
from apiglobo.converter import convert_virtuoso_response


virtuoso_response = {u'head': {u'link': [], u'vars': [u'property', u'value', u'nested_property', u'nested_value']}, u'results': {u'distinct': False, u'bindings': [{u'nested_property': {u'type': u'uri', u'value': u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'}, u'nested_value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/Comment'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/99954031-7b20-420a-a676-72ca23db047b'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/comment_body'}, u'nested_value': {u'type': u'literal', u'value': u'N\xe3o gostei muito n\xe3o brux\xe3o.'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/99954031-7b20-420a-a676-72ca23db047b'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/username'}, u'nested_value': {u'type': u'literal', u'value': u'Fulano'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/99954031-7b20-420a-a676-72ca23db047b'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/comments'}, u'nested_value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/reviews/cbeb23b6-bb58-496a-aa5b-462aee708ca0'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/99954031-7b20-420a-a676-72ca23db047b'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'}, u'nested_value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/Comment'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/0c65d435-cfa0-4b26-a02c-282fe65847c1'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/comment_body'}, u'nested_value': {u'type': u'literal', u'value': u'Eu sou o  brux\xe3o.'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/0c65d435-cfa0-4b26-a02c-282fe65847c1'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/username'}, u'nested_value': {u'type': u'literal', u'value': u'Beltrano'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/0c65d435-cfa0-4b26-a02c-282fe65847c1'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/comments'}, u'nested_value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/reviews/cbeb23b6-bb58-496a-aa5b-462aee708ca0'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/has_comment'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/comments/0c65d435-cfa0-4b26-a02c-282fe65847c1'}}, {u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/title'}, u'value': {u'type': u'literal', u'value': u'Windows 8: Hit or Miss ?'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'}, u'nested_value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/Software'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/revises'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/softwares/f45146cf-0a34-4b2e-a6ec-f7ec32dc4cdf'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/in_category'}, u'nested_value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/software-categories/OperatingSystem'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/revises'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/softwares/f45146cf-0a34-4b2e-a6ec-f7ec32dc4cdf'}}, {u'nested_property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/name'}, u'nested_value': {u'type': u'literal', u'value': u'Windows 8'}, u'property': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/schemas/revises'}, u'value': {u'type': u'uri', u'value': u'http://semantica.globo.com/tech/softwares/f45146cf-0a34-4b2e-a6ec-f7ec32dc4cdf'}}], u'ordered': True}}
expected_response = {
  "http://semantica.globo.com/tech/schemas/title": "Windows 8: Hit or Miss ?",
  "http://semantica.globo.com/tech/schemas/revises": {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Software",
    "http://semantica.globo.com/tech/schemas/in_category": "http://semantica.globo.com/tech/software-categories/OperatingSystem",
    "http://semantica.globo.com/tech/schemas/name": "Windows 8"
  },
  "http://semantica.globo.com/tech/schemas/has_comment": [
    {
    "http://semantica.globo.com/tech/schemas/comments": "http://semantica.globo.com/tech/reviews/cbeb23b6-bb58-496a-aa5b-462aee708ca0",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Comment",
    "http://semantica.globo.com/tech/schemas/comment_body": "Eu sou o  brux\u00e3o.",
    "http://semantica.globo.com/tech/schemas/username": "Beltrano"
    },
    {
    "http://semantica.globo.com/tech/schemas/comments": "http://semantica.globo.com/tech/reviews/cbeb23b6-bb58-496a-aa5b-462aee708ca0",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Comment",
    "http://semantica.globo.com/tech/schemas/comment_body": u'N\xe3o gostei muito n\xe3o brux\xe3o.',
    "http://semantica.globo.com/tech/schemas/username": "Fulano"
    }
  ]
}


class ConverterTestCase(unittest.TestCase):

    maxDiff = None

    def test_virtuoso_converter(self):
        response = convert_virtuoso_response(virtuoso_response)
        self.assertEquals(response, expected_response) 


if __name__ == "__main__":
    unittest.main()