# AWS Deployment (Part 4)

## Overview

The Trello Backend API was deployed on Amazon Web Services (AWS) using EC2, Amazon RDS, Docker, and Nginx.

The application architecture separates the application server from the database server by hosting the FastAPI application on an EC2 instance and PostgreSQL on Amazon RDS.

---

## AWS Services Used

- Amazon EC2 (Ubuntu 26.04)
- Amazon RDS (PostgreSQL)
- Amazon VPC
- Security Groups
- Docker
- Docker Compose
- Nginx
- GitHub

---

## Architecture

```text
                    Internet
                        │
                  HTTP / HTTPS
                        │
                  EC2 Public IP
                        │
                  Nginx (Port 80)
                        │
                  FastAPI (Port 8000)
                        │
                Amazon RDS PostgreSQL
                   (Private Database)
```

---

## Deployment Steps

### 1. Launch EC2 Instance

- Created an Ubuntu EC2 instance.
- Generated and downloaded an SSH key pair.
- Configured Security Groups:
  - Port 22 (SSH)
  - Port 80 (HTTP)
  - Port 443 (HTTPS)
  - Port 8000 (FastAPI)

---

### 2. Connect to EC2

```bash
chmod 400 <key>.pem

ssh -i <key>.pem ubuntu@<public-ip>
```

---

### 3. Install Docker

```bash
sudo apt update

sudo apt install docker.io docker-compose-v2 -y

sudo systemctl enable docker

sudo systemctl start docker

sudo usermod -aG docker ubuntu

newgrp docker
```

---

### 4. Create Amazon RDS

- Engine: PostgreSQL
- Connected RDS with the EC2 instance.
- Stored application data in Amazon RDS instead of a Docker PostgreSQL container.

If an initial database was not created during RDS setup, create it manually:

```sql
CREATE DATABASE task_management;
```

---

### 5. Clone Repository

```bash
git clone https://github.com/<username>/<repository>.git

cd Trello_Clone_API
```

---

### 6. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:<password>@<rds-endpoint>:5432/task_management
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CREATE_TABLES=1
```

---

### 7. Update Docker Compose

Removed the PostgreSQL service since the application now uses Amazon RDS.

Services deployed:

- FastAPI Backend
- Nginx Reverse Proxy

---

### 8. Deploy Application

```bash
docker compose up --build -d
```

Verify:

```bash
docker ps

docker compose logs backend
```

---

## Verification

Backend:

```text
http://<EC2-Public-IP>:8000/docs
```

Application:

```text
http://<EC2-Public-IP>
```

---

## Security

- SSH access restricted to the developer's public IP.
- RDS remains inside the VPC and is not publicly accessible.
- EC2 communicates with RDS through private networking.
- Nginx serves as the reverse proxy for FastAPI.

---

## Project Architecture

```text
GitHub Repository
        │
        ▼
      EC2 Instance
        │
    Docker Compose
        │
 ┌───────────────┐
 │     Nginx     │
 └───────┬───────┘
         │
 ┌───────▼───────┐
 │    FastAPI    │
 └───────┬───────┘
         │
         ▼
 Amazon RDS PostgreSQL
```

---

## Commands Used

```bash
ssh -i key.pem ubuntu@<public-ip>

git clone <repository>

docker compose up --build -d

docker compose logs backend

docker ps

docker compose down
```

---

## Outcome

- Successfully deployed the FastAPI backend on AWS EC2.
- Configured Nginx as a reverse proxy.
- Migrated PostgreSQL from Docker to Amazon RDS.
- Established secure communication between EC2 and RDS within the VPC.
- Verified the API using Swagger UI and ensured persistent database storage on Amazon RDS.