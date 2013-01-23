curl -i -X GET http://localhost:8890/sparql-auth?uri="/sparql-auth?default-graph-uri=&query=CLEAR+GRAPH+%3Chttp%3A%2F%2Fmythical_poc.globo.com%2F%3E+&should-sponge=&format=text%2Fhtml&timeout=0&debug=on" --digest --user api-semantica:api-semantica 

curl -i -X PUT http://localhost:5100/data/tech/schemas/SoftwareCategory -T "software_category.ttl" 
curl -i -X PUT http://localhost:5100/data/tech/schemas/Software -T "software.ttl" 
curl -i -X PUT http://localhost:5100/data/tech/schemas/Comment -T "comment.ttl" 
curl -i -X PUT http://localhost:5100/data/tech/schemas/Review -T "review.ttl"

curl -i -X POST http://localhost:5100/data/tech/softwares -H "Content-type: application/json" -T "software_instance.json" 
#curl -i -X POST http://localhost:5100/data/tech/reviews -H "Content-type: application/json" -T "review_win8_instance.json" 
#curl -i -X POST http://localhost:5100/data/tech/comments -H "Content-type: application/json" -T "comment_1_win8_instance.json" 
#curl -i -X GET http://localhost:5100/data/tech/reviews/d9153f71-a32b-45d7-a867-dbfdb307f936
