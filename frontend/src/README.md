# Full-Stack Project Management System

A modern full-stack web application featuring a FastAPI backend with SQLite/SQLAlchemy authentication and a responsive React Vite frontend dashboard.

---

## Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy, SQLite, Uvicorn, Pydantic, OAuth2 / Passlib (JWT Authentication)
* **Frontend:** React, Vite, JavaScript, CSS / Inline Styling

---

## Project Structure

```text
project-management-system/
│
├── backend/                  # FastAPI Backend API
│   ├── app/
│   │   ├── routers/          # API route handlers (auth, projects, tasks)
│   │   ├── database.py       # SQLAlchemy session and DB configuration
│   │   ├── models.py         # SQLAlchemy database models
│   │   ├── schemas.py        # Pydantic validation schemas
│   │   └── main.py           # FastAPI application entrypoint & CORS
│   └── requirements.txt      # Python dependencies
│
└── frontend/                 # React Vite Frontend
    ├── src/
    │   ├── App.jsx           # Main component & authentication views
    │   ├── main.jsx          # React entry point
    │   └── App.css           # Global stylesheet
    └── package.json          # Node dependencies