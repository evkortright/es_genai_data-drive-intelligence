# test-elasticsearch.py
from sources.elasticsearch import load_elasticsearch

es = load_elasticsearch()

print(es.info())
