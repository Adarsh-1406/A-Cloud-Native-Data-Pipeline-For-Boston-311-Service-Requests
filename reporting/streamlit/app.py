import streamlit as st

st.set_page_config(page_title="311 Service Requests", layout="wide")

pg = st.navigation([
    st.Page("dashboard.py", title="Visualization", icon=":material/chat:"), 
    st.Page("prediction.py", title="Case Duration Time", icon=":material/text_snippet:"),
    st.Page("llm.py", title="Text to SQL", icon=":material/assignment:")
    ])
pg.run()