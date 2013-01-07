Introduction
============

This is a proof-of-concept implementation developed to explore issues relevant
to the redesign of Globo.com platform infra-structure.


Requirements for the New Platform
=================================

  * single CMA 
  * integrated access to multiple databases (including different data models)
  # support for mobile apps


Objectives for this project
===========================

Design a draft of the new architecture for content publication.
Specify a draft for the interface contracts for:
 
  * CMA
  * Database integrator

Desired features
================

  * the definiton of data structures shoul carry its own documentation
  * versioning (which level: API, resource, ...)
  * Role-based access control (RBAC) model for authorization profiles 

    
Execution
=========

cd ./jsonform/

python -m SimpleHTTPServer
