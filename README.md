Introduction
============

This is a proof-of-concept implementation developed to explore issues relevant
to the redesign of Globo.com platform infra-structure.


Requirements for the New Platform
=================================

  Backend as a Service (BaaS) composed by cloud-based RESTful services:
  
    * unified CMA
    * uniform access to all enterprise data (CMS, Search, Semantics)
    * authentication
    * authorization
    * billing

  The new architeture should naturally lead to support for mobile apps

  API Requests (80%) should respond below 20ms.


Objectives for this project
===========================

 1) Draft of the new architecture for content publication.
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

Main concepts
====

Context
----

An isolated context of data, defined by some unique slug that defines its namespace.

It might represent, for example, the product or the app being developed.

Schema
---

As most of database models work with a clear distinction between instances (data) and
schema (metadata), we also make this distinction on the API interface.

Therefore, a *Schema* is a structure that defines the data being stored.

Schemas are defined in the RDF/OWL Model, given its high expressivity and flexibility. Like so,
it will be possible to represent schemas in different database models or even translations between them
in a common language.

Likewise, we expect a schema to be easily written, by using the Turtle format, the
most compact serialization of RDF/OWL models.

Instances
---

Instances must be easily retrieved and "instance queries" must be really simple
to developers to understand as they will do way more requests on instances than on schemas. As such,
the interface for manipulating instances also accept JSON as content_type as most of the APIs in
the wild do.

Execution
=========

cd ./jsonform/

python -m SimpleHTTPServer

Getting all data from all contexts
--------

*GET* 'http://localhost:5100/data/my_context/schemas/software' -H 'Content-type: application/json'

Add Data
--------

Adding schemas
---

```bash
POST 
```


Adding instances
---

```bash
```

Retrieving data
------------


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
