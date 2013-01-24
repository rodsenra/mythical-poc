Mythical POC
============

Cria schema de SoftwareCategory
-------------------------------

PUT /data/tech/schemas/SoftwareCategory

:SoftwareCategory a up:Schema ;
                  up:collectionName "software-categories" ;
                  rdfs:label "Categoria de Software"@pt .

:name a owl:DatatypeProperty ;
      rdfs:label "Nome"@pt ;
      rdfs:domain :SoftwareCategory ;
      rdfs:range xsd:string .

:has_software a  owl:ObjectProperty ;
              owl:inverseOf :in_category ;
              rdfs:domain :SoftwareCategory ;
              rdfs:range :Software .
              
Cria schema de Software
-----------------------

PUT /data/tech/schemas/Software

:Software a up:Schema ;
          owl:subClassOf up:Object,
                         dbpedia:Work ,
                         schema:CreativeWork ;
          owl:equivalentClass schema:SoftwareApplication ;
          up:collectionName "softwares" ;
          rdfs:label "Software"@pt .

:name a owl:DatatypeProperty ;
      owl:subPropertyOf up:name ;
      owl:equivalentProperty schema:name ;
      rdfs:label "Nome"@pt ;
      rdfs:domain :Software ;
      rdfs:range xsd:string .

:in_category a  owl:ObjectProperty ;
             owl:equivalentProperty schema:applicationCategory ;
             owl:inverseOf :has_software ;
             rdfs:domain :Software ;
             rdfs:range :SoftwareCategory .

Cria schema de Comment
----------------------

PUT /data/tech/schemas/Comment

:Comment a up:Schema ;
          owl:subClassOf up:Object,
                         dbpedia:Work ,
                         schema:CreativeWork ;
         up:collectionName "comments" ;
         rdfs:label "Comentário"@pt .

:username a owl:DatatypeProperty ;
          rdfs:label "Usuário"@pt ;
          rdfs:domain :Comment;
          rdfs:range xsd:string .

:comment_body a owl:DatatypeProperty ;
              rdfs:label "Corpo do comentário"@pt ;
              rdfs:domain :Comment;
              rdfs:range xsd:string .

:has_comment a owl:ObjectProperty ;
             rdfs:label "Comenta"@pt ;
             rdfs:domain :SoftwareReview;
             rdfs:range :Comment .

:comments a owl:ObjectProperty ;
          owl:inverseOf :has_comment ;
          rdfs:label "Comenta"@pt .
          
Cria schema de Review
---------------------

PUT /data/tech/schemas/Review

:SoftwareReview a up:Schema ;
                up:collectionName "reviews" ;
                rdfs:label "Review de Software"@pt .

:title a owl:DatatypeProperty ;
      rdfs:label "Título"@pt ;
      rdfs:domain :SoftwareReview ;
      rdfs:range xsd:string .

:revises a  owl:ObjectProperty ;
         rdfs:domain :SoftwareReview ;
         rdfs:range :Software .
