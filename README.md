# SHL AI Recommender System

## Overview

SHL AI Recommender System is an AI-powered conversational recommendation platform designed to help recruiters, hiring managers, and organizations discover the most suitable SHL assessments based on hiring requirements.

The system uses:
- Conversational clarification flow
- Semantic search using FAISS
- Intelligent recommendation ranking
- React-based modern UI
- FastAPI backend architecture

The platform understands hiring-related queries such as:
- Python Developer
- Machine Learning Engineer
- Backend Developer
- Database Administrator
- Java Spring Boot Developer
- Frontend Engineer

and recommends relevant SHL assessments dynamically.

---

# Features

## Conversational AI Hiring Assistant
- Multi-turn conversational interface
- Clarification-based interaction
- Dynamic recommendation generation

## Intelligent Recommendation Engine
- Semantic retrieval using FAISS
- Keyword scoring and ranking
- Role-specific filtering
- Seniority-aware recommendations

## SHL Assessment Recommendations
- Real SHL assessment URLs
- Test type categorization
- Job-level mapping
- Description-based matching

## Modern Frontend UI
- Responsive React interface
- Smooth auto-scroll chat
- Recommendation cards
- Loading animations
- Clean white/blue professional theme

## Backend API
- FastAPI-based REST API
- Modular architecture
- Scalable retrieval pipeline

---

# Problem Statement

Organizations often struggle to identify the correct SHL assessments for different hiring scenarios.

This project solves that problem using an AI-powered recommendation engine capable of:
- Understanding hiring intent
- Asking clarification questions
- Retrieving relevant SHL assessments
- Ranking assessments intelligently

---

# Tech Stack

## Frontend
- React.js
- Tailwind CSS
- Vite

## Backend
- FastAPI
- Python

## AI / Retrieval
- FAISS Vector Database
- HuggingFace Embeddings
- LangChain

## Data Processing
- JSON
- Semantic Embeddings
- Metadata Ranking

---

# System Architecture

```text
User Query
    ↓
Clarification Engine
    ↓
Conversation State Manager
    ↓
FAISS Semantic Retriever
    ↓
Recommendation Ranking Engine
    ↓
Filtered SHL Recommendations
    ↓
React Frontend UI

```
```
SHL_AI_Recommender/
│
├── app/
│   ├── agent/
│   │   ├── clarification_engine.py
│   │   ├── conversation_state.py
│   │   └── recommendation_engine.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── faiss_store.py
│   │
│   ├── routes/
│   │   └── chat.py
│   │
│   └── main.py
│
├── frontend/
│   └── vite-project/
│       ├── src/
│       │   ├── App.jsx
│       │   └── main.jsx
│       │
│       └── package.json
│
├── data/
│   ├── processed/
│   │   └── processed_catalog.json
│   │
│   └── vectorstore/
│       └── faiss_index/
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
```
# Core Components

Clarification Engine

Responsible for:

* Asking missing information
* Collecting role details
* Collecting seniority level

Example:

* “What role are you hiring for?”
* “What seniority level is this role for?”

⸻

# Conversation State Manager

Maintains:

* Current role
* Current seniority
* Query flow
* Multi-turn interaction context

⸻

# Recommendation Engine

Responsible for:

* Ranking SHL assessments
* Keyword scoring
* Semantic filtering
* Role-aware recommendation logic

⸻

# FAISS Retriever

Handles:

* Semantic search
* Vector similarity search
* Fast recommendation retrieval
