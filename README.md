# Hakon Backend

Backend API built with FastAPI for vulnerability management.

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and adjust values.

Run the application locally:

```bash
uvicorn app.main:app --reload
```
