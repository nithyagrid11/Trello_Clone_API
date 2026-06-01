# Trello Backend API

## Overview

This project is a Trello Backend API built using FastAPI, SQLAlchemy, and MySQL.
The application supports user authentication, board management, section management, ticket management, and invitation-based collaboration between users.

The system allows:

* Users to register and login using JWT authentication
* Board owners to create and manage boards
* Board owners to invite other users using invitation tokens
* Members to collaborate by creating and managing their own tickets
* Permission-based access control for owners and members

---

# Features

## Authentication

* User Registration
* User Login using JWT tokens
* Protected Routes using Bearer Authentication

---

## Boards

* Create Boards
* Get Boards associated with current user
* Get Detailed Board Information
* Invitation Token Generation
* Join Board using Invitation Token

---

## Sections

* Create Section
* Get Sections
* Update Section
* Delete Section

### Rules

* Parent board cannot be changed
* Only board owner can manage sections

---

## Tickets

* Create Ticket
* Get Tickets
* Update Ticket
* Delete Ticket

### Rules

* Ticket can move between sections only inside same board
* Members can only edit/delete tickets created by themselves
* Board owner can manage all tickets

---

## Collaboration

* Invitation Token System
* Board Membership System
* Owner and Member roles
* Permission-based access control

---

# Tech Stack

* Python
* FastAPI
* SQLAlchemy ORM
* MySQL
* Pydantic
* JWT Authentication
* Passlib (Password Hashing)
* Uvicorn

---

# Project Structure

```txt
app/
│
├── dependencies/
│   ├── auth.py
│   ├── database.py
│   └── permissions.py
│
├── models/
│   ├── user.py
│   ├── board.py
│   ├── section.py
│   ├── ticket.py
│   └── board_member.py
│
├── routes/
│   ├── auth.py
│   ├── users.py
│   ├── boards.py
│   ├── sections.py
│   └── tickets.py
│
├── schemas/
│   ├── user.py
│   ├── board.py
│   ├── section.py
│   ├── ticket.py
│   └── board_member.py
│
├── utils/
│   ├── jwt.py
│   └── password.py
│
├── config.py
├── database.py
└── main.py
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-url>

cd <project-folder>
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# MySQL Database Setup

## Create Database

Open MySQL terminal:

```bash
mysql -u root -p
```

Then create database:

```sql
CREATE DATABASE task_management;
```

---

# Environment Variables

Create a `.env` file in project root:

```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/task_management

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Run Application

```bash
python -m uvicorn app.main:app --reload
```

---

# Swagger API Documentation

Open:

```txt
http://127.0.0.1:8000/docs
```

---

# Authentication Flow

## Register User

Use:

```txt
POST /auth/register
```

---

## Login

Use Swagger `Authorize` button.

Enter:

* username = email
* password = user password

Swagger automatically stores JWT token.

---

# Invitation Flow

## Board Owner

1. Create board
2. Create sections
3. Generate invitation token

---

## Member

1. Register/Login
2. Join board using invitation token
3. View board details
4. Create and manage own tickets

---

# Permission Rules

## Board Owner

Can:

* Manage boards
* Manage sections
* Manage all tickets
* Invite users

---

## Board Members

Can:

* View board
* View tickets
* Create tickets
* Edit/Delete only their own tickets

Cannot:

* Edit boards
* Edit sections
* Edit others' tickets

---

# Generate Requirements File

pip freeze > requirements.txt

---

# GitHub Push Instructions

## Initialize Git

```bash
git init
```

---

## Add Files

```bash
git add .
```

---

## Commit

```bash
git commit -m "Initial commit"
```

---

## Add Remote Repository

```bash
git remote add origin <repository-url>
```

---

## Push to GitHub

```bash
git branch -M main

git push -u origin main
```

---

# API Endpoints

## Authentication

* `POST /auth/register`
* `POST /auth/login`

---

## Boards

* `POST /boards`
* `GET /boards`
* `GET /boards/{board_id}`
* `POST /boards/{board_id}/invite`
* `POST /boards/join/{token}`

---

## Sections

* `POST /sections`
* `GET /sections/board/{board_id}`
* `PUT /sections/{section_id}`
* `DELETE /sections/{section_id}`

---

## Tickets

* `POST /tickets`
* `GET /tickets/section/{section_id}`
* `PUT /tickets/{ticket_id}`
* `DELETE /tickets/{ticket_id}`

# Testing

This project includes both Unit Tests and Integration Tests to verify the correctness of utility functions, business logic, authentication, authorization, and API endpoints.

## Testing Tools Used

- Pytest
- pytest-cov
- FastAPI TestClient

---

## Test Database Setup

Create a separate MySQL database for testing:

```sql
CREATE DATABASE webframeworks_test;
```

Ensure MySQL is running before executing the tests.

---

## Install Testing Dependencies

```bash
pip install pytest pytest-cov httpx
```

Or install all project dependencies:

```bash
pip install -r requirements.txt
```

---

## Run All Tests

```bash
python -m pytest
```

---

## Run Coverage Report

```bash
python -m pytest --cov=app --cov-report=term-missing
```

This command displays:

- Total project coverage
- File-wise coverage
- Missing lines that are not covered by tests

---

## Unit Tests

The following files contain unit tests:

```text
app/tests/unit/test_password.py
app/tests/unit/test_jwt.py
app/tests/unit/test_permissions.py
```

### Covered Functions

- Password hashing
- Password verification
- JWT token generation
- JWT payload validation
- Ticket permission validation

---

## Integration Tests

The following files contain integration tests:

```text
app/tests/integration/tests_auth_routes.py
app/tests/integration/test_user_routes.py
app/tests/integration/test_boards_route.py
app/tests/integration/test_section_route.py
app/tests/integration/test_tickets_route.py
```

### Covered Endpoints

Authentication:
- POST /auth/register
- POST /auth/login

Users:
- GET /users/me

Boards:
- POST /boards

Sections:
- POST /sections

Tickets:
- POST /tickets

---

## Test Fixtures

Shared test fixtures are defined in:

```text
app/tests/conftest.py
```

These fixtures:

- Create a fresh test database session
- Reset database tables before each test
- Override FastAPI database dependency
- Provide a reusable TestClient instance

---

## Current Coverage

The project currently achieves over 80% total test coverage, exceeding the required minimum coverage of 50%.

Example:

```text
TOTAL 81%
```

---

## Running a Single Test File

Examples:

```bash
python -m pytest app/tests/unit/test_password.py -v
```

```bash
python -m pytest app/tests/unit/test_jwt.py -v
```

```bash
python -m pytest app/tests/integration/tests_auth_routes.py -v
```

```bash
python -m pytest app/tests/integration/test_boards_route.py -v
```

---

## Notes

- Unit tests validate individual functions in isolation.
- Integration tests validate complete API workflows using FastAPI TestClient.
- A dedicated test database is used to avoid affecting production data.