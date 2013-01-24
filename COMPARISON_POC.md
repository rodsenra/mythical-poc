# Mythical POC

## Schemas

### Cria schema de Software

```
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
```

### Cria schema de Comment

```
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
```

### Cria schema de Review

```
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

```

## Instâncias

### Cria instância de Software

```
POST /data/tech/softwares

{
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Software",
    "http://semantica.globo.com/tech/schemas/name": "Windows 8",
    "http://semantica.globo.com/tech/schemas/in_category": "http://semantica.globo.com/tech/software-categories/OperatingSystem"
}
```

### Cria instância de Review

```
POST /data/tech/reviews

{
    "http://semantica.globo.com/tech/schemas/title": "Windows 8: Hit or Miss ?",
    "http://semantica.globo.com/tech/schemas/revises": "http://semantica.globo.com/tech/softwares/a3f8b8e4-f44b-4e11-b236-62911301639d"
}
```

### Cria instância de Comment

```
POST /data/tech/comments

{
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Comment",
    "http://semantica.globo.com/tech/schemas/username": "Fulano",
    "http://semantica.globo.com/tech/schemas/comment_body": "Não gostei muito não bruxão.",
    "http://semantica.globo.com/tech/schemas/comments": "http://semantica.globo.com/tech/reviews/d9153f71-a32b-45d7-a867-dbfdb307f936"
}
```

## Consulta

### Review

```
GET /data/tech/reviews/<slug>

{
  "http://semantica.globo.com/tech/schemas/title": "Windows 8: Hit or Miss ?",
  "http://semantica.globo.com/tech/schemas/revises": {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Software",
    "http://semantica.globo.com/tech/schemas/in_category": "http://semantica.globo.com/tech/software-categories/OperatingSystem",
    "http://semantica.globo.com/tech/schemas/name": "Windows 8",
    "uri": "http://semantica.globo.com/tech/softwares/bca3f378-f690-473b-b006-0d667abe8c28"
  },
  "http://semantica.globo.com/tech/schemas/has_comment": [
    {
      "http://semantica.globo.com/tech/schemas/comments": "http://semantica.globo.com/tech/reviews/e7a0078f-28fb-4a27-8af3-5e0909ea5a69",
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Comment",
      "http://semantica.globo.com/tech/schemas/comment_body": "N\u00e3o gostei muito n\u00e3o brux\u00e3o.",
      "uri": "http://semantica.globo.com/tech/comments/33d6b9ac-92be-4edd-b11d-a7c0e2f2c702",
      "http://semantica.globo.com/tech/schemas/username": "Fulano"
    },
    {
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://semantica.globo.com/tech/schemas/Comment",
      "http://semantica.globo.com/tech/schemas/comments": "http://semantica.globo.com/tech/reviews/e7a0078f-28fb-4a27-8af3-5e0909ea5a69",
      "uri": "http://semantica.globo.com/tech/comments/f786eb71-3f41-4f69-84d0-95af988de553",
      "http://semantica.globo.com/tech/schemas/replies": "http://semantica.globo.com/tech/comments/33d6b9ac-92be-4edd-b11d-a7c0e2f2c702",
      "http://semantica.globo.com/tech/schemas/username": "Beltrano",
      "http://semantica.globo.com/tech/schemas/comment_body": "Eu sou o  brux\u00e3o."
    }
  ]
}
```
