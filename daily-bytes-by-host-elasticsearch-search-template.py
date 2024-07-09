# daily-bytes-by-host-elasticsearch-search-template.py
from sources.elasticsearch import load_elasticsearch

es = load_elasticsearch()

params = {
  "interval": "1d"
}

results = es.search_template(
  index = "kibana_sample_data_logs",
  id = "bytes-by-host",
  params = params
)
print(results)
