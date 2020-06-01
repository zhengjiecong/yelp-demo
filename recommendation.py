from flask import Flask
from flask import request
from elasticsearch import Elasticsearch

app = Flask(__name__)

#id=ZqsUkDmt7duCN0KAJk8ESQ
@app.route('/similar_business')
def similar_business():
	business_index = 'yelp_business'
	result = {}
	try:
		id = request.args.get('id','')
		es = Elasticsearch(['192.168.1.175:9200'])
		re = es.get(index=business_index, id=id)
		query_vec = re['_source']['features']
		query_str = "(NOT business_id: "+id+") AND (NOT photo_url:*images*)"
		query_string = {
			"query": {
				"script_score": {
					"query" : { 
						"query_string": {
							"query": query_str
						}
					},
					"script": {
						"source": "cosineSimilarity(params.vector,doc['features'])+1.0",
						"params": {
							"vector": query_vec
						}
					}
				}
			}
		}
		result = es.search(index=business_index, body=query_string)
	except:
		result = {}
	return result
	
