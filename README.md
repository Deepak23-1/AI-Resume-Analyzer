# AI Resume Analyzer

## Overview

AI Resume Analyzer is a FastAPI-based backend application that allows users to register, log in securely using JWT authentication, upload PDF resumes, extract text from resumes, store them in PostgreSQL, and analyze them using Google's Gemini AI.

## Features

- User Registration
- User Login (JWT Authentication)
- Password Hashing
- Protected APIs
- Resume Upload (PDF)
- PDF Text Extraction using PyPDF
- Store Resume in PostgreSQL
- Resume History API
- Get Resume by ID
- AI Resume Analysis using Gemini
- ATS Score
- Technical Skills
- Missing Skills
- Strengths
- Weaknesses
- Improvement Suggestions

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- PyPDF
- Google Gemini AI
- Pydantic

## Project Structure

```
AI_Resume_Analyzer/
│
├── app/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── uploads/
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

## Installation

```bash
git clone <repository-url>

cd AI_Resume_Analyzer

pip install -r requirements.txt
```

## Run Project

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

## Authentication

This project uses JWT Authentication.

Login to obtain an access token and use the Authorize button in Swagger UI to access protected APIs.

## Future Improvements

- Resume vs Job Description Matching
- Save AI Analysis History
- Admin Dashboard
- Role-Based Authorization
- Docker Support
- Cloud Deployment