# sources.elasticsearch.py
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv()

CLOUD_ID = os.getenv("CLOUD_ID")
CLOUD_USER_ID = os.getenv("CLOUD_USER_ID")
CLOUD_USER_PASSWORD = os.getenv("CLOUD_USER_PASSWORD")

def load_elasticsearch():
    es = Elasticsearch (
        cloud_id=os.getenv("CLOUD_ID"),
        basic_auth=(os.getenv("CLOUD_USER_ID"), os.getenv("CLOUD_USER_PASSWORD"))
    )
    return es

# es = load_elasticsearch()
