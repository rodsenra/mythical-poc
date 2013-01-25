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

  For the data acess layer, the main concern of this project, API Requests (80%) should respond below 20ms.

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

References
==========

 * https://github.com/globocom/mysqlapi
 * Cloud CMS http://code.cloudcms.com/javascript-samples/#/components/node-type

Desired features
================

  * The definiton of data structures shoul carry its own documentation
  * Versioning (which level: API, resource, ...)
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

Collection
--

A schema defines a group of instances of the same type, hereby named a collection.

Instance
---

Instances must be easily retrieved and "instance queries" must be really simple
to developers to understand as they will do way more requests on instances than on schemas. As such,
the interface for manipulating instances also accept JSON as content_type as most of the APIs in
the wild do.

Execution
=========

cd ./jsonform/

python -m SimpleHTTPServer

In all examples from now on we use a context named *tech* and a
a collection named *software*.

Data Model of the example
==========

    * A Software has a name.
    * A Software has a category.

    * A Review has a title.
    * A Review might be about a Software.
    * A Review has a rating about the sotware it refers to.
    * A Review also has comments associated to it.

    * A comment has a user name.
    * A comment has a text body.

Interface examples
======

List all contexts and operations
--------

```http
GET 'http://localhost:5100/data'
```

List all schemas of a context
---

```http
GET 'http://localhost:5100/data/tech/schemas'
```

Get a specific schema of a context
---

```http
GET 'http://localhost:5100/data/tech/schemas/software'
```

Create schema
---

```http
PUT 'http://localhost:5100/data/tech/schemas/software' -H 'Content-type: text/turtle'
```

The payload for this request will be something like:

    :Software a up:Schema ;
          owl:subClassOf up:Object,
                         dbpedia:Work ,
                         schema:CreativeWork ;
          owl:equivalentClass schema:SoftwareApplication ;
          up:collectionName "softwares" ;
          rdfs:label "Software"@pt .

Adding instances
---

```http
POST 'http://localhost:5100/data/tech/software' -H 'Content-type: application/json'
```

Example of payload:

```json
{
    "rdfs:type": "tech_schemas:Software",
    "tech_schemas:name": "Windows 8",
    "tech_schemas:in_category": "tech:software-categories/OperatingSystem"
}
```

-=|  TODO  |=- URI prefix resolution

Setup before using Virtuoso
---------------------------

CREATE GRAPH <http://mythical_poc.globo.com>
