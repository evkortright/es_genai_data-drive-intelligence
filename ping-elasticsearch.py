# ping-elasticsearch.py
import time
from sources.elasticsearch import load_elasticsearch

es = load_elasticsearch()

while True:
    startTime = time.time()
    es.ping()
    endTime = time.time()
    latency = (endTime - startTime) * 1000
    print(f"latency: {latency:.5f}ms")
    time.sleep(1)
