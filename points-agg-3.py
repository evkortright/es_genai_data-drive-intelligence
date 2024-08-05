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
    res = es.search_template(index="kibana_sample_data_logs", id = "change-points-search")
    return res

# Extract data from the JSON
data = load_data()

buckets = data['aggregations']['by_day']['buckets']
st.write('buckets:')
st.json(buckets)

dates = [bucket['key_as_string'] for bucket in buckets]
# Convert dates to datetime objects
dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") for date in dates]
st.write('dates:')
st.json(dates)

averages = [bucket['avg_bytes']['value'] for bucket in buckets]
st.write('averages:')
st.json(averages)
