# University Management System – FastAPI

This project is a RESTful API for managing **students**, **professors**, and **courses** in a university system.

The backend is built using **FastAPI** and **SQLModel**, containerized with **Docker**, and served behind **Nginx** as a reverse proxy.

---

## 🚀 Features
- CRUD operations for:
  - Students
  - Professors
  - Courses
- Strong data validation (Persian names, national ID, phone numbers, etc.)
- SQLite database
- Docker & Docker Compose setup
- Nginx reverse proxy

---

## 🧱 Tech Stack
- Python 3.11
- FastAPI
- SQLModel
- Pydantic
- Uvicorn
- Docker & Docker Compose
- Nginx

---

## 📦 Project Structure
```text

├── main.py
├── Dockerfile
├── Dockerfile.nginx
├── docker-compose.yml
├── nginx.conf
├── database.db
├── requirements.txt
└── README.md

