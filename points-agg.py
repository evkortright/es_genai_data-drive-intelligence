# points-agg.py
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from sources.elasticsearch import load_elasticsearch
from models.models import load_gpt4, load_gpt3_5
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
import json

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
st.json(data.body)

buckets = data['aggregations']['by_day']['buckets']
dates = [bucket['key_as_string'] for bucket in buckets]
averages = [bucket['avg_bytes']['value'] for bucket in buckets]

# Convert dates to datetime objects
dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") for date in dates]

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
# plt.show()

st.header("ESRE Engineer Change-Points Advisor")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Change-Points Chart")
    st.pyplot(fig)

with col2: 
    # llm = load_gpt4()
    llm = load_gpt3_5()

    template = """You are a helpful Elasticsearch expert assistant.
    The Elasticsearch change point aggregation is a sibling pipeline aggregation that detects, spikes, dips, and change points in a metric. Given a distribution of values provided by the sibling multi-bucket aggregation, this aggregation indicates the bucket of any spike or dip and/or the bucket at which the largest change in the distribution of values, if they are statistically significant.
    These are the results of the change point aggregation.
    {context}
    The first "hit" is a sample document from a logs index.

    Question: {question}
    """
    question = "Please interpret and analyze the aggregation results and provide recommended next steps. Include a DSL query that could be used to further explore any spikes or dips found. For the DSL query please use kibana_sample_data_logs as the name of the index to search."
    prompt = ChatPromptTemplate.from_template(template)
    parser = StrOutputParser()
    chain = prompt | llm | parser

    st.subheader("Analysis and Advice")
    st.chat_message("user").markdown(question)
    with st.spinner('Analyzing...'):
        answer = chain.invoke({"context": data, "question": question})
        st.balloons()
    st.chat_message("assistant").markdown(answer)

st.chat_input()