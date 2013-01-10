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

    
Execution
=========

cd ./jsonform/

python -m SimpleHTTPServer

curl -i -XPOST 'http://localhost:5100/data/reviews' -H "Content-Type: application/json"  -d '{"title":"Novissimo Bla"}'
curl -i -XPOST 'http://localhost:5100/schemas' -H "Content-Type: application/json"  -T "schemas/review_schema.json"
