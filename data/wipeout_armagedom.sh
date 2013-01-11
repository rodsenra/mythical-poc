curl -i -X POST  'http://localhost:7474/db/data/cypher' -H 'Content-type: application/json' -d '{"query": "start no=relationship(*) delete no"}'
curl -i -X POST  'http://localhost:7474/db/data/cypher' -H 'Content-type: application/json' -d '{"query": "start no=node(*) delete no"}'
curl -i -X DELETE  http://localhost:9200/data