# Archaeology News Insight Engine

An automated news aggregation and analysis system for archaeological discoveries and research, featuring real-time updates, location mapping, and AI-powered insights.

## Architecture Overview
![Architecture Diagram](https://github.com/user-attachments/assets/9e2402d3-0f35-49b3-bc25-85287cf31c01)

## Architecture Doodle 😄
![Planning Sketch](https://github.com/user-attachments/assets/0a28319b-4cc8-4502-82ac-34aedf15602e)

## Features

* **Real-time News Collection**: Automated collection of archaeology news from multiple sources
* **Content Enrichment**: Full-text extraction and location detection
* **Interactive Map**: Geographical visualization of archaeological discoveries
* **AI-Powered Q&A**: Natural language queries about recent archaeological findings
* **Automated Orchestration**: Scheduled data collection and processing pipelines

## System Architecture & Tools

### Data Collection 
* Cloud Function-based NewsAPI integration
* Duplicate detection and filtering
* GitHub Actions for scheduled collection

### Content Enrichment & Geocoding
* Full-text extraction using newspaper3k
* Geocoding pipeline for coordinate mapping
* Location entity extraction using spaCy

### Data Ingestion and Storage
* Pub/Sub topic publication for new articles
* BigQuery storage for enriched content and main Database

### Orchestration 
* Cron Jobs through Github Actions Workflow

### Frontend Interface
* Built on Streamlit

### LLM Integration
* Code Llama for SQL query generation
* Mistral AI for insights generation

## Acknowledgments

* NewsAPI for data access
* Huggingface Inference API for access to AI models
* GCP for infrastructure
* Streamlit for Frontend and deployment

---
*Note: This project was built as part of exploring modern AI and cloud technologies in archaeological news aggregation.*
