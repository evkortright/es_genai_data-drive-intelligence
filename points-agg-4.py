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
# st.write('buckets:')
# st.json(buckets)

dates = [bucket['key_as_string'] for bucket in buckets]
# Convert dates to datetime objects
dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") for date in dates]
# st.write('dates:')
# st.json(dates)

averages = [bucket['avg_bytes']['value'] for bucket in buckets]
# st.write('averages:')
# st.json(averages)

# dark theme:
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor']='darkgray'
plt.rcParams['text.color']='white'
plt.rcParams['xtick.color']='white'
plt.rcParams['ytick.color']='white'

# Create the line chart
fig = plt.figure(figsize=(10, 7))
plt.plot(dates, averages, marker='o', markersize = 4)

# Extract the change point
change_point_date = data['aggregations']['change_points_avg']['bucket']['key']
change_point_date = datetime.strptime(change_point_date, "%Y-%m-%dT%H:%M:%S.%fZ")
change_point_avg = data['aggregations']['change_points_avg']['bucket']['avg_bytes']['value']

# Annotate the change point```python
# Check if it's a dip or spike
if 'dip' in data['aggregations']['change_points_avg']['type']:
    plt.annotate('DIP', (mdates.date2num(change_point_date), change_point_avg), textcoords="offset points", xytext=(10,10), ha='center', color='red')
elif 'spike' in data['aggregations']['change_points_avg']['type']:
    plt.annotate('SPIKE', (mdates.date2num(change_point_date), change_point_avg), textcoords="offset points", xytext=(10,10), ha='center', color='green')

plt.gcf().autofmt_xdate()

st.subheader("Change-Points Chart")
st.pyplot(fig)
