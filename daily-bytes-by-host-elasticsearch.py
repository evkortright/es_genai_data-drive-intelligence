# daily-bytes-by-host-elasticsearch.py
from sources.elasticsearch import load_elasticsearch

es = load_elasticsearch()

body = {
  "size": 0,
  "aggregations": {
    "by_host": {
      "terms": {
        "field": "host.keyword"
      },
      "aggs": {
        "by_day": {
          "date_histogram": {
            "field": "@timestamp",
            "calendar_interval": "1d"
          }
        }
      }
    }
  }
}

results = es.search(index = "kibana_sample_data_logs", body = body)
print(results)
