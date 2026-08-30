# 🧠 Company Knowledge Intelligence

> **Production-oriented RAG + LLM application for intelligent question answering over company documents.**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![AWS ECS](https://img.shields.io/badge/AWS-ECS%20Fargate-orange.svg)](https://aws.amazon.com/ecs/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black.svg)](https://github.com/features/actions)
[![Tests](https://img.shields.io/badge/Tests-89%20Passed-success.svg)](#testing)

---

## 🚀 Live Demo

### 🌐 Streamlit Application

👉 **[Open Company Knowledge Intelligence](https://company-knowledge-intelligence-2uj6rkvkqbnmdrkwmcnbwb.streamlit.app/)**

### 📦 GitHub Repository

👉 **[View Source Code](https://github.com/creatorKrishna05/company-knowledge-intelligence)**

---

## 📌 Overview

**Company Knowledge Intelligence** is a production-oriented **Retrieval-Augmented Generation (RAG)** application designed to answer questions from company documents.

The system processes PDF documents, converts their content into embeddings, stores them for semantic retrieval, retrieves the most relevant information for a user query, and provides that context to an LLM to generate a grounded response.

The application also provides **source and page information** to improve answer traceability.

---

## 🎯 Problem Statement

Company information is often distributed across documents such as:

* Employee handbooks
* HR policies
* Company guidelines
* Internal documentation
* Product documentation
* Business reports

Searching these documents manually can be slow and inefficient.

This project provides an AI-powered knowledge interface where users can simply ask questions in natural language and retrieve relevant information from the company's document knowledge base.

---

## 🔄 RAG Pipeline

text
                    Company PDF
                         │
                         ▼
                ┌─────────────────┐
                │ Document        │
                │ Ingestion       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Cleaning   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Chunking        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Embeddings      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Vector Store    │
                └────────┬────────┘
                         │
                         │
User Query ──────────────┤
                         ▼
                ┌─────────────────┐
                │ Retrieval       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Context Builder │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ LLM             │
                │ Groq / Ollama   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Answer + Source │
                │ + Page          │
                └─────────────────┘


---

## ✨ Key Features

* 📄 PDF document ingestion
* 🧹 Text cleaning and normalization
* ✂️ Recursive document chunking
* 🧠 Hugging Face embeddings
* 🔎 Semantic similarity retrieval
* 🤖 LLM-powered question answering
* 📚 Context-aware responses
* 📍 Source and page references
* 🔐 Secure API key management
* 🐳 Dockerized application
* ☁️ AWS ECS Fargate deployment
* 📦 Amazon ECR container registry
* 🔑 AWS Secrets Manager
* 🧪 Automated testing
* 🔄 CI/CD with GitHub Actions
* 🖥️ Streamlit interface

---

# 🏗️ System Architecture

text
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         └───────────┬──────────┘
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │    RAG Pipeline      │
                         └───────────┬──────────┘
                                     │
                ┌────────────────────┴────────────────────┐
                │                                         │
                ▼                                         ▼
      ┌──────────────────┐                     ┌──────────────────┐
      │ Document         │                     │ User Query       │
      │ Ingestion        │                     └────────┬─────────┘
      └────────┬─────────┘                              │
               ▼                                        ▼
      ┌──────────────────┐                     ┌──────────────────┐
      │ Text Cleaning    │                     │ Query Embedding  │
      └────────┬─────────┘                     └────────┬─────────┘
               ▼                                        │
      ┌──────────────────┐                              │
      │ Chunking         │                              │
      └────────┬─────────┘                              │
               ▼                                        │
      ┌──────────────────┐                              │
      │ Embedding Model  │                              │
      └────────┬─────────┘                              │
               │                                        │
               └────────────────┬───────────────────────┘
                                ▼
                     ┌──────────────────────┐
                     │    Vector Store      │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Relevant Chunks      │
                     │ Retrieval            │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Context Builder      │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Groq / Ollama LLM    │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Answer + Citations   │
                     └──────────────────────┘


---

# 🛠️ Technology Stack

| Category             | Technology          |
| -------------------- | ------------------- |
| Programming Language | Python              |
| LLM Providers        | Groq, Ollama        |
| Embeddings           | Hugging Face        |
| AI Architecture      | RAG                 |
| Frontend             | Streamlit           |
| Testing              | Pytest              |
| Containerization     | Docker              |
| Container Registry   | Amazon ECR          |
| Cloud Deployment     | AWS ECS Fargate     |
| Secrets Management   | AWS Secrets Manager |
| CI/CD                | GitHub Actions      |
| Version Control      | Git & GitHub        |

---

# 📂 Project Structure

text
company-knowledge-intelligence/
│
├── app/
│   ├── chunking/
│   │   └── recursive_chunker.py
│   │
│   ├── cleaning/
│   │   └── text_cleaner.py
│   │
│   ├── embedding/
│   │   ├── base.py
│   │   └── huggingface.py
│   │
│   ├── ingestion/
│   │   └── loaders/
│   │       └── pdf_loader.py
│   │
│   ├── indexing_service.py
│   └── knowledge_ingestion_service.py
│
├── domain/
│   └── documents.py
│
├── data/
│
├── tests/
│
├── streamlit_app.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .gitignore
└── README.md


---

# 🔬 RAG Workflow

## 1. Document Ingestion

PDF documents are loaded and converted into structured document objects.

Each document contains content and useful metadata such as:

* Source
* Page number
* Document information

---

## 2. Text Cleaning

Extracted text is normalized to remove unnecessary whitespace and formatting noise.

This improves the quality of downstream chunking and retrieval.

---

## 3. Chunking

Large documents are divided into smaller chunks using recursive chunking.

Chunking helps the retrieval system find focused and relevant information instead of passing entire documents to the LLM.

---

## 4. Embeddings

Each document chunk is converted into a numerical vector representation using a Hugging Face embedding model.

These vectors capture the semantic meaning of the text.

---

## 5. Vector Storage

The generated embeddings are stored in the vector store.

The vector representation allows the application to perform semantic similarity search.

---

## 6. Retrieval

When a user submits a question:

text
User Question
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
Top Relevant Chunks


The most relevant chunks are retrieved from the knowledge base.

---

## 7. Context Building

The retrieved chunks are combined into a structured context.

This context is passed to the LLM along with the user's question.

---

## 8. LLM Generation

The LLM generates the final answer based on the retrieved context.

Supported providers include:

* **Groq**
* **Ollama**

This abstraction makes it possible to change the LLM provider without changing the complete RAG architecture.

---

## 9. Source Attribution

The application returns source/page information along with the answer.

This improves:

* Transparency
* Traceability
* User confidence
* Grounding

---

# 🤖 Why RAG?

A general-purpose LLM may not have access to private company information.

RAG solves this problem by connecting an LLM to an external knowledge base.

text
Company Documents
       ↓
Embeddings
       ↓
Vector Store
       ↓
Relevant Information
       ↓
LLM Context
       ↓
Grounded Answer


### RAG vs Fine-Tuning

| RAG                            | Fine-Tuning                               |
| ------------------------------ | ----------------------------------------- |
| Retrieves external knowledge   | Changes model behavior/weights            |
| Easy to update documents       | Requires retraining/update process        |
| Good for private knowledge     | Good for specialized behavior             |
| Can provide sources            | Sources are not inherent                  |
| Suitable for dynamic knowledge | Better for consistent task/style behavior |

---

# 🔐 Security

The application does **not hardcode API keys**.

Sensitive credentials are stored as environment variables/secrets.

### Local Development

text
GROQ_API_KEY
HF_TOKEN


### AWS Deployment

Secrets are managed through:

text
AWS Secrets Manager
        ↓
ECS Task Definition
        ↓
Container Environment


Secrets are never committed to GitHub or included directly inside the Docker image.

---

# 🐳 Docker

The application is containerized using Docker.

### Build Image

bash
docker build -t company-knowledge-intelligence .


### Run Container

bash
docker run -p 8501:8501 company-knowledge-intelligence


### Local Application

text
http://localhost:8501


---

# ☁️ AWS Deployment

The application is deployed using AWS container infrastructure.

text
GitHub
   │
   ▼
Docker Build
   │
   ▼
Amazon ECR
   │
   ▼
Amazon ECS
   │
   ▼
AWS Fargate
   │
   ▼
Running Container


### AWS Services

#### Amazon ECR

Used to store and manage the Docker container image.

#### Amazon ECS

Used to manage the application container as a service.

#### AWS Fargate

Provides serverless container execution without managing EC2 servers.

#### AWS Secrets Manager

Used to securely store:

text
GROQ_API_KEY
HF_TOKEN


#### CloudWatch

Used for container/application logs and troubleshooting.

---

# 🔄 CI/CD

GitHub Actions is used to automate the development workflow.

text
Developer Push
      ↓
GitHub
      ↓
GitHub Actions
      ↓
Automated Tests
      ↓
Docker Build
      ↓
Container Image
      ↓
Deployment


This creates a repeatable deployment workflow and reduces manual deployment steps.

---

# 🧪 Testing

The project includes automated tests using **Pytest**.

### Latest Test Result

text
89 passed


Tests cover important application components including:

* PDF ingestion
* Text cleaning
* Chunking
* Embedding/indexing
* RAG services
* Core application behavior

---

# 🖥️ Running Locally

## 1. Clone Repository

bash
git clone https://github.com/creatorKrishna05/company-knowledge-intelligence.git


bash
cd company-knowledge-intelligence


## 2. Create Virtual Environment

bash
python -m venv .venv


### Windows

bash
.venv\Scripts\activate


## 3. Install Dependencies

bash
pip install -r requirements.txt


## 4. Configure Environment Variables

Create a `.env` file locally:

text
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token


> Never commit `.env` to GitHub.

## 5. Run Streamlit

bash
streamlit run streamlit_app.py


The application will be available at:

text
http://localhost:8501


---

# 📊 Engineering Practices

The project follows production-oriented software engineering principles including:

* Modular architecture
* Separation of responsibilities
* Dependency abstraction
* Environment-based configuration
* Secure secret management
* Automated testing
* Containerization
* CI/CD
* Cloud deployment

The architecture is designed to make individual components easier to test, replace, and maintain.

---

# 🎯 Interview Highlights

This project demonstrates practical experience with:

### AI / ML

* Retrieval-Augmented Generation
* Large Language Models
* Embeddings
* Semantic Search
* Vector Retrieval
* Prompt Engineering
* Context Building
* Grounded Generation

### Python

* Object-Oriented Programming
* Modular architecture
* Abstract interfaces
* Dependency management
* Exception handling
* Unit testing

### Cloud / DevOps

* Docker
* Amazon ECR
* Amazon ECS
* AWS Fargate
* AWS Secrets Manager
* CloudWatch
* GitHub Actions
* CI/CD

### Development

* Git
* GitHub
* Pytest
* Streamlit
* API integration

---

# 💡 Key Learning

Through this project, I gained hands-on experience building an AI application from **document ingestion to cloud deployment**.

The project helped me understand how individual RAG components work together in a production-oriented system:

text
Data
 ↓
Ingestion
 ↓
Cleaning
 ↓
Chunking
 ↓
Embeddings
 ↓
Retrieval
 ↓
Context
 ↓
LLM
 ↓
Answer
 ↓
Deployment


---

# 🚀 Future Improvements

Potential future enhancements include:

* RAG evaluation framework
* Retrieval re-ranking
* Hybrid search
* Advanced vector database
* Agentic RAG
* MCP integration
* Voice interface
* Multi-document management
* Advanced observability
* Response quality evaluation
* Authentication and user management

---

# 👨‍💻 Author

## Kanchan Nishad

Aspiring **AI/ML Engineer** focused on:

* Machine Learning
* Generative AI
* LLMs
* Retrieval-Augmented Generation
* Python
* Cloud & MLOps

### 🔗 Links

* **Live Demo:** https://company-knowledge-intelligence-2uj6rkvkqbnmdrkwmcnbwb.streamlit.app/
* **GitHub:** https://github.com/creatorKrishna05/company-knowledge-intelligence

---

# ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
