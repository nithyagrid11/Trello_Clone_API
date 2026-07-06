# Trello Backend API

## Overview

A Trello-like Backend API built using FastAPI, SQLAlchemy, PostgreSQL, and Docker.

The application supports:

* User Authentication with JWT
* Board Management
* Section Management
* Ticket Management
* Invitation-Based Collaboration
* Role-Based Access Control

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* SQLite (Testing)
* JWT Authentication
* Passlib
* Docker
* Docker Compose
* Nginx
* Pytest

---

## Project Structure

```text
app/
├── dependencies/
├── models/
├── routes/
├── schemas/
├── tests/
├── utils/
├── config.py
├── database.py
└── main.py
```

---

## Setup

### Clone Repository

```bash
git clone <repository-url>
cd <project-folder>
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/task_management
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Database tables are created automatically when the app starts.

---

## Run Locally

```bash
python -m uvicorn app.main:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Docker Setup

The application is containerized using:

* FastAPI Backend
* PostgreSQL Database
* Nginx Reverse Proxy

Start containers:

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

Architecture:

```text
Browser
   ↓
 Nginx
   ↓
FastAPI
   ↓
PostgreSQL
```

---

## API Endpoints

### Authentication

* POST `/auth/register`
* POST `/auth/login`

### Users

* GET `/users/me`

### Boards

* POST `/boards`
* GET `/boards`
* GET `/boards/{board_id}`
* POST `/boards/{board_id}/invite`
* POST `/boards/join/{token}`

### Sections

* POST `/sections`
* GET `/sections/board/{board_id}`
* PUT `/sections/{section_id}`
* DELETE `/sections/{section_id}`

### Tickets

* POST `/tickets`
* GET `/tickets/section/{section_id}`
* PUT `/tickets/{ticket_id}`
* DELETE `/tickets/{ticket_id}`

---

## Testing

Run all tests:

```bash
python -m pytest
```

Run coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Coverage: **80%+**

Runtime uses PostgreSQL, while tests use SQLite (`test.db`) for fast and isolated execution.

---

## Notes

* Passwords are securely hashed using Passlib.
* JWT is used for authentication and authorization.
* Docker Compose manages FastAPI, PostgreSQL, and Nginx services.
* Permission-based access control is implemented for boards, sections, and tickets.
