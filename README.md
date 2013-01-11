Introduction
============

This is a proof-of-concept implementation developed to explore issues relevant
to the redesign of Globo.com platform infra-structure.


Requirements for the New Platform
=================================

  Backend as a Service (BaaS) composed by cloud-based RESTful services: 
    * unified CMA 
    * uniform access to all enterprise data (CMS,Search, Semantics)
    * authentication 
    * authorization
    * billing
    
  The new architeture should naturally lead to support for mobile apps


Objectives for this project
===========================

 1) Design a draft of the new architecture for content publication.
    Define a first version of the interfaces and contracts between the
    several components of the architecture.
    There is no need for a complete implementation at the end of the project.
    Development of code will be done on-demand to validate concepts.
 
 2) The design of the architecture will define the communication between the teams.
    We should be able to understand which stories are relevant to which teams. 

  The outcome of this project should be to deliver a draft implementation that
  does CMA+CDA for some content using the base elements of new architecture.
  The focus will be to elucidate doubts about the new architecture.

Data Model
==========

  Review <----> Software <-----> Categoria
     |                 \----------> Rating
     |
     \- Title
      \- Comments -> Comment


References
==========

 * https://github.com/globocom/mysqlapi

Desired features
================

  * the definiton of data structures shoul carry its own documentation
  * versioning (which level: API, resource, ...)
  * Role-based access control (RBAC) model for authorization profiles 

Configuration
=============
 We applied two configurations in ElasticSearch:
  - elasticsearch/config/default-mapping.json 
  - elasticsearch/config/elasticsearch.yml
 
 This files are inside the mythical-poc project tree, below config/elasticsearch. 
 The goal of the configuration is to define that "uid" field always has exact match.
 
Execution
=========

cd ./jsonform/

python -m SimpleHTTPServer

curl -i -XPUT  'http://localhost:5100/data/schemas/review_schema' -H 'Content-type: application/json' -T ./data/review_schema.json
curl -i -XPUT  'http://localhost:5100/data/schemas/software_schema' -H 'Content-type: application/json' -T ./data/software_schema.json

HTTP/1.0 201 CREATED
Content-Type: text/html; charset=utf-8
Location: http://localhost:5100/data/schema/review_schema
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: PUT, HEAD, OPTIONS, GET
Access-Control-Max-Age: 21600
Content-Length: 0
Server: Werkzeug/0.8.3 Python/2.7.1
Date: Thu, 10 Jan 2013 18:03:30 GMT

Clean-up ElasticSearch
----------------------
  curl -X DELETE http://localhost:9200/data

Clean-up Neo4j
--------------
  start no=relationship(*) delete no;
  start no=node(*) delete no;

Query ES
--------
  curl -XGET 'http://localhost:9200/data/_search?q=uid:"/data/schemas/software"&pretty=true'


Deprecated
==========

 curl -i -XPOST 'http://localhost:5100/data/reviews' -H "Content-Type: application/json"  -d '{"title":"Novissimo Bla"}'
 curl -i -XPOST 'http://localhost:5100/schemas' -H "Content-Type: application/json"  -T "schemas/review_schema.json"
