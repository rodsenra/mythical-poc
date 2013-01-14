curl -i -XPUT  'http://localhost:5100/data/schemas/software' -H 'Content-type: application/json' -T software_schema.json
curl -i -XPUT  'http://localhost:5100/data/schemas/comment' -H 'Content-type: application/json' -T comment_schema.json
curl -i -XPUT  'http://localhost:5100/data/schemas/review' -H 'Content-type: application/json' -T review_schema.json
curl -i -XPOST  'http://localhost:5100/data/softwares' -H 'Content-type: application/json' -T software_instance.json
# curl -i -XPOST  'http://localhost:5100/data/reviews' -H 'Content-type: application/json' -T review_win8_instance.json
