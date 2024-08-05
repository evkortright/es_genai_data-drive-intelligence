# points-agg-1.py
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from sources.elasticsearch import load_elasticsearch
from models.models import load_gpt4, load_gpt3_5
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

st.set_page_config(layout="wide")

es = load_elasticsearch()

@st.cache_data
def load_data():
    res = es.search(index="kibana_sample_data_logs", body= {
    "size": 0, 
    "aggs": {
        "by_day":{ 
            "date_histogram": {
                "field": "@timestamp",
                "fixed_interval": "1d"
            },
            "aggs": {
                "avg_bytes": { 
                    "avg": {
                        "field": "bytes"
                    }
                }
            }
        },
        "change_points_avg": { 
            "change_point": {
                "buckets_path": "by_day>avg_bytes" 
            }
        }
    }
    }
    )

    return res

# Extract data from the JSON
data = load_data()
st.write('Results:')
st.json(data.body)
