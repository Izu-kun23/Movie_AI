# Quick Start Guide

## Project Structure

```
Movie_AI/
├── backend/          # All Python files here
│   ├── main.py      # FastAPI server
│   ├── model.py     # ML model
│   ├── movies.csv   # Movie database
│   └── ...
└── frontend/        # All frontend files here
    ├── index.html
    └── ...
```

## Quick Start

### 1. Start the Backend Server

```bash
cd backend
uvicorn main:app --reload
```

Or use the run script:
```bash
cd backend
python run_server.py
```

Server will start at: **http://127.0.0.1:8000**

### 2. Open the Frontend

Simply open `frontend/index.html` in your browser!

Or build the frontend first:
```bash
cd frontend
npm install
npm run build
```

Then open `frontend/index.html`

### 3. Chat with the AI!

In the chat interface, try:
- "I like The Matrix"
- "Recommend movies similar to Inception"
- "Search for Batman"

## Running from Different Directories

### From project root:
```bash
cd backend && uvicorn main:app --reload
```

### From backend directory:
```bash
uvicorn main:app --reload
```

Both work because all paths are relative to the backend folder!

