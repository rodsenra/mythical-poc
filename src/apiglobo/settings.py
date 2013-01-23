# -*- coding: utf-8 -*-
import logging


DEBUG = True

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5100

#ES_ENDPOINT = 'http://localhost:9200'  
#NEO4J_ENDPOINT = "http://localhost:7474/db/data/"

DEFAULT_GRAPH = "http://mythical_poc.globo.com/"
BASE_URI = 'http://semantica.globo.com'

SPARQL_ENDPOINT_REALM = "SPARQL"  # Virtuoso-related
SPARQL_ENDPOINT_AUTH_MODE = "digest"  # 'basic', ''
SPARQL_ENDPOINT_AUTH = "http://localhost:8890/sparql-auth"
SPARQL_ENDPOINT_USER = "api-semantica"
SPARQL_ENDPOINT_PASSWORD = "api-semantica"

LOG_FILE = "/tmp/apiglobo.log"
LOG_LEVEL = logging.DEBUG
LOG_NAME = "apiglobo"
