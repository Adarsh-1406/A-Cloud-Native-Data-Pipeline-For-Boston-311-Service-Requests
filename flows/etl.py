# The ETL job orchestrator

# imports
import requests
from prefect import flow, task

# helper function - generic invoker
def invoke_gcf(url: str, payload: dict):
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

@task(retries=2)
def schema_department_assignment():
    """Setup the stage schema"""
    url = "https://us-central1-group2-ba882.cloudfunctions.net/group2-schema-department_assignment"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def schema_location():
    """Setup the stage schema"""
    url = "https://us-central1-group2-ba882.cloudfunctions.net/group2-schema-location"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def schema_requests():
    """Setup the stage schema"""
    url = "https://us-central1-group2-ba882.cloudfunctions.net/group2-schema-requests"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def schema_response_time():
    """Setup the stage schema"""
    url = "https://us-central1-group2-ba882.cloudfunctions.net/group2-schema-response_time"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def schema_status_history():
    """Setup the stage schema"""
    url = "https://us-central1-group2-ba882.cloudfunctions.net/group2-schema-status_history"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def extract():
    """Extract the RSS feeds into JSON on GCS"""
    url = "https://us-central1-group2-ba882.cloudfunctions.net/group2-extract"
    resp = invoke_gcf(url, payload={})
    return resp

@task(retries=2)
def load(payload):
    """Load the tables into the raw schema, ingest new records into stage tables"""
    url = "https://us-central1-group2-ba882.cloudfunctions.net/group2-load"
    resp = invoke_gcf(url, payload=payload)
    return resp

# Prefect Flow
@flow(name="311-service-requests-etl-flow", log_prints=True)
def etl_flow():
    """The ETL flow which orchestrates Cloud Functions"""

    result1 = schema_department_assignment()
    print("Schema setup for department assignment completed")

    result2 = schema_location()
    print("Schema setup for location completed")

    result3 = schema_requests()
    print("Schema setup for requests completed")

    result4 = schema_response_time()
    print("Schema setup for response time completed")

    result5 = schema_status_history()
    print("Schema setup for status history completed")
    
    extract_result = extract()
    print("Data extracted onto GCS")
    
    # Pass extract_result as payload to load function
    load_result = load(payload=extract_result)
    print("The data were loaded into the raw schema and changes added to stage")

# the job
if __name__ == "__main__":
    etl_flow()