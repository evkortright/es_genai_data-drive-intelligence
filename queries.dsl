# Daily bytes by host
GET kibana_sample_data_logs/_search
{
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

# Generalized and templatized
PUT _scripts/bytes-by-host
{
  "script": {
    "lang": "mustache",
    "source": {
      "size": 0,
      "aggregations": {
        "by_host": {
          "terms": {
            "field": "host.keyword"
          },
          "aggs": {
            "by_{{interval}}": {
              "date_histogram": {
                "field": "@timestamp",
                "calendar_interval": "{{interval}}"
              }
            }
          }
        }
      }
    }
  }
}

# Render the template before using it
POST _render/template
{
  "id": "bytes-by-host",
  "params": {
    "interval": "20d"
  }
}

# Search invoking the template
GET kibana_sample_data_logs/_search/template
{
  "id": "bytes-by-host",
  "params": {
    "interval": "1d"
  }
}