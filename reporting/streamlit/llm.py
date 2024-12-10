import streamlit as st
import duckdb
import json
from vertexai.generative_models import GenerativeModel, Content, Part, GenerationConfig
# imports
import streamlit as st 
import json
import networkx as nx 
import matplotlib.pyplot as plt

from google.cloud import secretmanager
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import GenerationConfig

GCP_PROJECT = 'group2-ba882'
project_id = 'group2-ba882'
GCP_REGION = "us-central1"

#from pinecone import Pinecone, ServerlessSpec
import duckdb

version_id = 'latest'
# secret manager motherduck
sm = secretmanager.SecretManagerServiceClient()
vector_name = f"projects/{project_id}/secrets/project_key/versions/latest"
response = sm.access_secret_version(request={"name": vector_name})
md_token = response.payload.data.decode("UTF-8")
# Initialize MotherDuck connection
conn = duckdb.connect(f'md:city_services_boston?motherduck_token={md_token}')

# Define table info - using stage schema
schema_name = "stage"
tables = ["case_duration", "department_assignment", "locations", 
          "requests", "response_time", "status_history"]

# Initialize GenAI model
model = GenerativeModel(model_name="gemini-1.5-flash-002")
generation_config = GenerationConfig(temperature=0, response_mime_type="application/json")

# Streamlit App UI
st.title("Interactive SQL Query Generator with GenAI")
st.markdown("Enter your query prompt, and the system will generate and execute the corresponding SQL on MotherDuck.")

# Add table selection dropdown
selected_table = st.selectbox("Select table:", tables)
fully_qualified_table = f"city_services_boston.stage.{selected_table}"

user_input = st.text_area("Enter your query prompt:", "")

# Handle user input
if st.button("Generate and Execute SQL Query"):
    if user_input:
        # Fetch schema from MotherDuck
        try:
            schema_query = f"DESCRIBE {fully_qualified_table}"
            schema_result = conn.execute(schema_query).fetchall()
            schema = {row[0]: row[1] for row in schema_result}
        except Exception as e:
            st.error(f"Error fetching schema: {e}")
            schema = {}

        # Construct the schema description and prompt
        if schema:
            schema_description = "\n".join([f"{name} ({dtype})" for name, dtype in schema.items()])
            prompt = f"""
            You are a SQL expert. Based on the user's input and the provided schema, generate a valid SQL query.
            Use the table `{fully_qualified_table}`. Ensure the query references the table and its columns correctly.
            Return the result as a valid JSON with a key `SQL` containing the SQL query.

            ### Schema
            {schema_description}

            ### User Prompt
            {user_input}

            ### SQL Query (as JSON)
            """

            # Use GenAI to generate the SQL query
            user_prompt_content = Content(
                role="user",
                parts=[Part.from_text(prompt)],
            )

            try:
                response = model.generate_content(user_prompt_content, generation_config=generation_config)

                # Extract the generated SQL query from the response
                llm_query = json.loads(response.text)
                sql_query = llm_query.get("SQL")

                if sql_query:
                    # Display the generated SQL query
                    st.markdown("### Generated SQL Query")
                    st.code(sql_query)

                    # Execute the SQL query against MotherDuck
                    try:
                        result = conn.execute(sql_query).fetchdf()

                        # Remove rows with null values
                        df_cleaned = result.dropna()

                        # Display the query results
                        st.markdown("### Query Results")
                        st.dataframe(df_cleaned)  # Show result table
                    except Exception as e:
                        st.error(f"An error occurred while executing the query: {e}")
                else:
                    st.error("No SQL query was generated.")
            except Exception as e:
                st.error(f"Error generating the SQL query: {e}")
        else:
            st.error("Failed to fetch schema from MotherDuck.")
    else:
        st.warning("Please enter a query prompt.")

# Close the MotherDuck connection
conn.close()