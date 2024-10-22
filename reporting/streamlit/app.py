import streamlit as st
import duckdb
import pandas as pd
from google.cloud import secretmanager
import numpy as np

from itertools import combinations
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt

project_id = 'group2-ba882'
secret_id = 'project_key'   #<---------- this is the name of the secret you created
version_id = 'latest'

db = 'awsblogs'
schema = "stage"
db_schema = f"{db}.{schema}"

sm = secretmanager.SecretManagerServiceClient()

name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

response = sm.access_secret_version(request={"name": name})
md_token = response.payload.data.decode("UTF-8")

md = duckdb.connect(f'md:?motherduck_token={md_token}') 

############################################ Streamlit App

st.set_page_config(page_title="My Fancy Streamlit App", layout="wide")

sql = """
select 
    min(published) as min,
    max(published) as max,
from
    awsblogs.stage.posts
"""
date_range = md.sql(sql).df()
start_date = date_range['min'].to_list()[0]
end_date = date_range['max'].to_list()[0]


st.title("Streamlit - 882")
st.subheader("To demonstrate concepts - It's just a python script!")


st.sidebar.header("Filters")
st.sidebar.markdown("One option is to use sidebars for inputs")
author_filter = st.sidebar.text_input("Search by Author")
date_filter = st.sidebar.date_input("Post Start Date", (start_date, end_date))

st.sidebar.button("A button to control inputs")

st.sidebar.file_uploader("Users can upload files that your app analyzes!")

st.sidebar.markdown("These controls are not wired up to control data, just highlighting you have a lot of control!")


############ A simple line plot

num_days = 365  # Number of days for the time series
start_date = '2023-01-01'  # Start date

date_range = pd.date_range(start=start_date, periods=num_days, freq='D')

np.random.seed(42)  # For reproducibility
values = np.random.randint(50, 150, size=num_days)  # Example: random sales values between 50 and 150

time_series_data = pd.DataFrame({
    'date': date_range,
    'value': values
})

st.line_chart(time_series_data, x="date", y="value")

############ Graph of co-association of tags, a touch forward looking
st.markdown("---")

pt_sql = """
select post_id, term from awsblogs.stage.tags
"""
pt_df = md.sql(pt_sql).df()

st.markdown("### You _can_ show data tables")
st.dataframe(pt_df)

st.markdown("### A static network graph")
st.markdown("We can think of relationships as a graph")

cotag_pairs = []

for _, group in pt_df.groupby('post_id'):
    # Get the unique list of authors for each post
    terms = group['term'].unique()
    # Generate all possible pairs of co-authors for this post
    pairs = combinations(terms, 2)
    cotag_pairs.extend(pairs)

cotag_counter = Counter(cotag_pairs)

G = nx.Graph()

for (term1, term2), weight in cotag_counter.items():
    G.add_edge(term1, term2, weight=weight)

degree_centrality = nx.degree_centrality(G)

node_sizes = [100 * degree_centrality[node] for node in G.nodes()]

edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

pos = nx.spring_layout(G, k=0.3, seed=42)  

fig = plt.figure(figsize=(12, 12))

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)

nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray')

plt.title("Tag Graph")
st.pyplot(fig)


############ There are some chat support features, more coming

st.markdown("---")

st.markdown("### There is even some chat features - more coming on the roadmap.")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")