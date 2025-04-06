# Building A Cloud-Native Data Pipeline: Integrating Boston 311 Data For Real-Time Insights

## BA882 Deploying Analytics Pipelines

## About:
🌆 **Boston 311 Cloud-Native Data Pipeline**
**Real-time Analytics** | **Geospatial Dashboards** | **ML Predictions** | **Text-to-SQL LLMs**

📌 **Overview**  
This project presents an end-to-end cloud-native data pipeline developed for managing and analyzing Boston 311 service request data. The goal was to build a robust, scalable architecture that could not only process over 100,000+ daily records in real-time but also deliver actionable insights through predictive modeling, interactive dashboards, and LLM-powered querying.  

It was built as part of the "Deploying Analytics Pipelines" course at Boston University (Fall 2024), with a focus on solving real-world civic tech challenges using modern data engineering and analytics tools.

🔧 **Tech Stack**  
- **Google Cloud Platform (GCP)** – BigQuery, Cloud Storage, Cloud Functions  
- **MotherDuck** – Modern cloud-native OLAP engine (based on DuckDB)  
- **Prefect** – Orchestrating ETL workflows  
- **Streamlit** – Interactive dashboards for real-time decision-making  
- **Mapbox** – Geospatial visualizations for resource allocation  
- **Apache Superset** – Data exploration and self-service BI  
- **Scikit-learn (Random Forest Regression)** – Forecasting resolution times  
- **LLMs (Text-to-SQL)** – Natural language interface for non-technical users  

🎯 **Key Features**

🔄 **Real-time Data Ingestion & Transformation**  
- Ingested and processed 100k+ daily service request records using GCP pipelines with Prefect orchestration  
- Structured & stored the transformed data using MotherDuck for blazing-fast analytics  

🧠 **ML-Powered Forecasting**  
- Built and deployed a Random Forest Regression model to predict Case Resolution Times with 87% accuracy  
- Helped reduce SLA non-compliance and improve response prioritization  

🗺️ **Geospatial & Visual Analytics**  
- Integrated Mapbox with Streamlit to build real-time, interactive maps showing complaint density, priority clusters, and more  
- Empowered stakeholders to visually track trends and optimize city resource allocation  

🧠 **Text-to-SQL LLM Integration**  
- Integrated a natural language querying layer enabling non-technical users to ask questions like "Which neighborhoods have the most unresolved pothole requests?"  
- Reduced manual querying time by 30%, democratizing access to insights  

📊 **Impact**  
✅ Increased operational transparency for city officials  
✅ Reduced SLA violations by 18% via predictive alerting  
✅ Enabled self-service analytics for business users and citizens  
✅ Enhanced citizen satisfaction through better response planning
