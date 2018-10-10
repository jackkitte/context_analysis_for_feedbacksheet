import pprint
import ptvsd
from elasticsearch import Elasticsearch

ptvsd.enable_attach(address=("0.0.0.0", 3000))
ptvsd.wait_for_attach()
ptvsd.break_into_debugger()

es = Elasticsearch("elasticsearch:9200")

result = es.search(index="feedbacksheet", 
                   body={"query": {
                            "query_string": {
                                "query": 'cause:1 AND phenomenon:"障害"'
                            }
                         },
                         "size": 10000,
                        }
                   )
print(len(result["hits"]["hits"]))
#pprint.pprint(result)