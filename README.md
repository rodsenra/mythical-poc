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

  API Requests (80%) should respond below 20ms.


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

Add Data
--------

Adding data to a schema-instance database
--

In our project, we distinguish adding instances (data) or schema (metadata).

Given the difference between classes and individuals in database models like relational
databases or a triplestore based on OWL, or, in other terms, given that classes are
first-class citizens in these models, we have two distinct data insertion points to desambiguate
these two aspects.

Adding schemas
---



Adding instances
---

jisadssjidsa


Retrieving data
------------

LALLALALALAL

```bash
curl -i -XPUT  'http://localhost:5100/data/schemas/software' -H 'Content-type: application/json' -T software_schema.json
```

```bash
curl -i -XPUT  'http://localhost:5100/data/schemas/review' -H 'Content-type: application/json' -T review_schema.json
```

```bash
curl -i -XPOST  'http://localhost:5100/data/softwares' -H 'Content-type: application/json' -T software_instance.json
```

Query textual data
------------------
curl -i -X GET "http://localhost:5100/data/reviews?q=\"windows\""

List supported query languages
------------------------------

curl -i -XGET 'http://localhost:5100/data/query'


Query using Cypher
------------------
  curl -i -X GET  "http://localhost:5100/data/query/cypher" -H "Content-type: application/json" -T cypher_query.json

Query using Gremlin
-------------------
  curl -i -X GET  "http://localhost:5100/data/query/gremlin" -H "Content-type: application/json" -d "g.v(37).map()"

Clean-up ElasticSearch
----------------------
  curl -X DELETE http://localhost:9200/data

Query ES
--------
  curl -XGET 'http://localhost:9200/data/_search?q=uid:"/data/schemas/software"&pretty=true'

Clean-up Neo4j
--------------
  start no=relationship(*) delete no;
  start no=node(*) delete no;

Setup before using Virtuoso
---------------------------
  create graph <http://mythical_poc.globo.com>


Deprecated
==========

 curl -i -XPOST 'http://localhost:5100/data/reviews' -H "Content-Type: application/json"  -d '{"title":"Novissimo Bla"}'
 curl -i -XPOST 'http://localhost:5100/schemas' -H "Content-Type: application/json"  -T "schemas/review_schema.json"
