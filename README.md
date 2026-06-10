````markdown
# Cosmetic Ingredients Analysis with RAG and LLM

## Overview

This project is an intelligent assistant for analyzing cosmetic ingredients using Large Language Models and Retrieval-Augmented Generation.

The goal is to help users search, understand and interpret information related to cosmetic ingredients from a document-based knowledge base.

## Main Objectives

- Analyze cosmetic ingredient information.
- Retrieve relevant content using semantic search.
- Generate contextual answers using an LLM.
- Organize cosmetic knowledge through a vector database.
- Provide a simple web interface for user interaction.

## Technologies Used

- Python
- Flask
- LangChain
- FAISS
- Gemini LLM
- Embeddings
- HTML
- CSS
- RAG
- NLP

## Project Structure

```text
cosmetic-ingredients-rag-analysis/
│
├── app.py
├── README.md
├── requirements.txt
├── data/
├── index/
├── static/
├── templates/
└── instance/
````

## How It Works

The system uses a RAG approach. Documents are processed and transformed into embeddings, then stored in a FAISS vector index.
When a user asks a question, the system retrieves the most relevant information and uses a language model to generate an answer.

## Features

* Cosmetic ingredient question answering
* Semantic search
* Document-based retrieval
* Contextual answer generation
* Flask web interface

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Then open the application locally in your browser.

## Note

The system provides AI-generated answers based on available documents. The responses should be verified before being used for medical, dermatological or regulatory decisions.

```
```
