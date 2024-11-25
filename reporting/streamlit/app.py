import streamlit as st
import duckdb
import pandas as pd
from google.cloud import secretmanager
import numpy as np
from datetime import datetime  # <-- Importing datetime module
from PIL import Image

from itertools import combinations
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt

# Google Cloud Secret Manager setup
project_id = 'group2-ba882'
secret_id = 'project_key'   #<---------- this is the name of the secret you created
version_id = 'latest'

db = 'awsblogs'
schema = "stage"
db_schema = f"{db}.{schema}"

# Accessing secrets from Google Cloud Secret Manager
sm = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
response = sm.access_secret_version(request={"name": name})
md_token = response.payload.data.decode("UTF-8")

# Connecting to DuckDB using the token from Secret Manager
md = duckdb.connect(f'md:?motherduck_token={md_token}') 

############################################ Streamlit App

# Set page configuration with custom icon and layout
st.set_page_config(
    page_title="PREDICT 311", 
    page_icon="https://play-lh.googleusercontent.com/-ei9jmjQa4C0dLIciwW3BF9Ym0M7_tjJlmlrDX3SxPQ7y5qflwWUsaGxuRzZyJBFZwg",  # Local icon path or URL if hosted online
    layout="wide"
)

# SQL query to get date range (min and max published dates)
sql = """
select 
    min(published) as min,
    max(published) as max,
from
    awsblogs.stage.posts
"""
date_range = md.sql(sql).df()

# Extracting start_date and end_date from the query result
start_date = date_range['min'].to_list()[0]
end_date = date_range['max'].to_list()[0]

# Check if 'min' or 'max' dates are NaT and replace them with today's date if necessary
if pd.isna(start_date):
    start_date = datetime.today()  # Replace NaT with today's date

if pd.isna(end_date):
    end_date = datetime.today()  # Replace NaT with today's date

# Convert start_date and end_date to proper date format if needed (optional)
start_date = pd.to_datetime(start_date).date()
end_date = pd.to_datetime(end_date).date()

# Streamlit Title and Subheader
st.markdown("<h1 style='font-size: 36px;'>PREDICT 311: Service Request Duration Predictor</h1>", unsafe_allow_html=True)

# Bold Introduction using markdown
st.markdown("**INTRODUCTION**")

# Reduced description size and aligned text as justified using HTML/CSS
st.markdown("""
<div style='text-align: justify; font-size: 14px;'>
Welcome to PREDICT 311, your go-to tool for predicting service request durations in Boston's 311 Service Requests System. 
This app leverages advanced machine learning models to estimate the time it will take to resolve a service request based on its case inquiry ID. 
Whether you're a city official or a curious citizen, PREDICT 311 provides quick and reliable insights into expected service completion times, 
helping you plan and manage requests, resources more efficiently.
</div>
""", unsafe_allow_html=True)

st.write("\n" * 2)  # Adds three newlines

# --- NEW CODE FOR DROPDOWN STARTS HERE ---
# SQL query to get unique values from the 'source' column in 'stage.requests'
query = """
SELECT DISTINCT source 
FROM city_services_boston.stage.requests
"""

# Execute the query and fetch the results into a pandas DataFrame
source_df = md.execute(query).fetchdf()

# Extract the 'source' column as a list for the dropdown options
source_list = source_df['source'].tolist()

# Create a dropdown in Streamlit using st.selectbox()
selected_source = st.selectbox("Select Source", options=source_list)

# Display the selected source
st.write(f"You selected: {selected_source}")
# --- END OF NEW CODE FOR DROPDOWN ---



# Sidebar filters for user inputs
st.sidebar.header("Filters")
st.sidebar.markdown("Use Dynamic Filtering Options for customized data view")
author_filter = st.sidebar.text_input("Search by Case Enquiry ID")

# Add a unique key to the date_input widget to avoid duplicate element IDs
date_filter = st.sidebar.date_input("Search by Date Range", (start_date, end_date), key="post_start_date")

st.sidebar.button("A button to control inputs")
st.sidebar.file_uploader("Users can upload files that your app analyzes!")
#st.sidebar.markdown("These controls are not wired up to control data, just highlighting you have a lot of control!")

############ A simple line plot

num_days = 365  # Number of days for the time series
start_date_for_plot = pd.to_datetime('2023-01-01')  # Replace with actual start_date if needed

date_range_for_plot = pd.date_range(start=start_date_for_plot, periods=num_days, freq='D')

np.random.seed(42)  # For reproducibility in random data generation
values = np.random.randint(50, 150, size=num_days)  # Example: random sales values between 50 and 150

time_series_data = pd.DataFrame({
    'Month': date_range_for_plot,
    'Number of Cases': values
})

# Displaying line chart in Streamlit using time series data
st.line_chart(time_series_data, x="Month", y="Number of Cases")

############ Graph of co-association of tags, a touch forward looking
st.markdown("---")

pt_sql = """
select post_id, term from awsblogs.stage.tags
"""
pt_df = md.sql(pt_sql).df()

# Displaying data table in Streamlit using dataframe
st.markdown("### Prediction Performance Metrics")
st.markdown("A Drill down description of the Cases")
st.dataframe(pt_df)

# Static network graph visualization for tag co-association
st.markdown("### A static network graph")
st.markdown("We can think of relationships as a graph")

cotag_pairs = []

for _, group in pt_df.groupby('post_id'):
    # Get the unique list of terms for each post (assuming these are tags)
    terms = group['term'].unique()
    # Generate all possible pairs of co-occurring tags for this post (combinations of two)
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