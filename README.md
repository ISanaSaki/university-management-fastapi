# 🎓 University Management System API

A comprehensive **University Management System** built with **FastAPI**, **SQLModel**, and **SQLite**, featuring complete data validation for Iranian educational standards, Docker containerization, and Nginx reverse proxy deployment.

This system provides RESTful API endpoints for managing students, professors, and courses with robust data integrity and validation according to Iranian national standards.

---

## 🚀 Features

-   ✨ **Complete CRUD Operations** for Students, Professors, and Courses
-   ✨ **Comprehensive Data Validation** for Iranian national standards
-   ✨ **SQLite Database** with SQLModel ORM
-   ✨ **RESTful API** with FastAPI framework
-   ✨ **Dockerized Deployment** with multi-container setup
-   ✨ **Nginx Reverse Proxy** for production-ready deployment
-   ✨ **Automatic Database Initialization** on startup
-   ✨ **Input Sanitization & Error Handling** with Persian error messages

---

## 🛠 Tech Stack

-   **Backend Framework:** FastAPI 0.110+
-   **ORM & Database:** SQLModel with SQLite
-   **Data Validation:** Pydantic 2.0+
-   **ASGI Server:** Uvicorn 0.27+
-   **Containerization:** Docker & Docker Compose
-   **Reverse Proxy:** Nginx
-   **Language:** Python 3.11+

---

## 📂 Project Structure

```
project/
├── main.py              # FastAPI application with all endpoints
├── Dockerfile           # FastAPI application container
├── Dockerfile.nginx     # Nginx web server container
├── docker-compose.yml   # Multi-container orchestration
├── nginx.conf           # Nginx reverse proxy configuration
├── database.db          # SQLite database file (auto-generated)
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

---

## 🐳 Docker Deployment

### Prerequisites
- Docker installed on your system
- Docker Compose installed

### Quick Start
```bash
# Clone and navigate to project directory
docker-compose up --build
```

### Services
The system runs two services:
1. **Backend** (`backend:8080`) - FastAPI application
2. **Nginx** (`nginx:80`) - Reverse proxy and web server

### Access Points
- **API Documentation:** http://localhost/docs
- **Interactive API Docs:** http://localhost/redoc
- **API Endpoints:** http://localhost/api

---

## 🧪 Development Setup

### Local Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### Database
The SQLite database (`database.db`) is automatically created and initialized when the application starts for the first time.

---

## 🔧 API Endpoints

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students/` | Create a new student |
| GET | `/students/` | List all students (with pagination) |
| GET | `/students/{stid}` | Get student by ID |
| PUT | `/students/{stid}` | Update student information |
| DELETE | `/students/{stid}` | Delete a student |

### Professors
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/professors/` | Create a new professor |
| GET | `/professors/` | List all professors (with pagination) |
| GET | `/professors/{lid}` | Get professor by ID |
| PUT | `/professors/{lid}` | Update professor information |
| DELETE | `/professors/{lid}` | Delete a professor |

### Courses
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/courses/` | Create a new course |
| GET | `/courses/` | List all courses (with pagination) |
| GET | `/courses/{cid}` | Get course by ID |
| PUT | `/courses/{cid}` | Update course information |
| DELETE | `/courses/{cid}` | Delete a course |

---

## 📝 Data Validation Rules

### Student Validation
- **Student ID:** 11 digits (`YYY114150XX` format)
  - First 3 digits: Entry year (385-403, representing 1385-1403)
  - Middle 6 digits: Must be "114150"
  - Last 2 digits: Unique identifier
- **Names:** Persian characters only, max 10 characters
- **Father's Name:** Persian characters only, max 10 characters
- **National ID:** 10-digit Iranian national code
- **Birth Date:** Jalali (Solar Hijri) calendar format (`YYYY/MM/DD`)
- **Birth City:** Valid Iranian provincial capital
- **Phone Numbers:** Iranian mobile (`09xxxxxxxxx`) and landline formats
- **Postal Code:** 10-digit number
- **Marital Status:** "مجرد" (Single) or "متاهل" (Married)

### Professor Validation
- **Professor ID:** 6-digit number
- **Names:** Persian characters only, max 10 characters
- **National ID:** 10-digit Iranian national code
- **Department:** One of "فنی مهندسی", "علوم پایه", or "اقتصاد"
- **Major:** Valid major corresponding to the department

### Course Validation
- **Course ID:** 5-digit number
- **Course Name:** Persian characters only, max 25 characters
- **Department:** One of "فنی مهندسی", "علوم پایه", or "اقتصاد"
- **Credit Units:** Integer between 1 and 4

---

## 🏗️ Models

### Base Person Model
Contains common attributes for both Students and Professors:
- Personal information (name, national ID, birth details)
- Contact information (address, phone numbers)
- Academic information (department, major)

### Student Model
Extends Person with:
- Student-specific ID (11-digit)
- Father's name
- ID card details (serial number, letter, code)
- Marital status
- Course and professor associations

### Professor Model
Extends Person with:
- Professor-specific ID (6-digit)
- Course associations

### Course Model
Independent model for course management:
- Course ID
- Course name
- Department
- Credit units

---

## 🔒 Security & Validation

### Input Validation
- All inputs are validated using Pydantic validators
- Persian character validation for names
- Iranian phone number format validation
- Date format validation (Jalali calendar)
- National ID and postal code validation

### Error Handling
- Comprehensive Persian error messages
- HTTP status codes for different error types
- Input sanitization to prevent injection attacks

### Database Security
- SQL injection protection through SQLModel ORM
- Type-safe queries
- Transaction management

---

## 🌐 Nginx Configuration

The system uses Nginx as a reverse proxy with the following features:
- Port forwarding (80 → backend:8080)
- Header forwarding for client information
- HTTP to HTTPS readiness (SSL certificate support)
- Load balancing ready configuration

---

## 📊 Pagination & Filtering

All list endpoints support pagination:
- `offset`: Number of records to skip
- `limit`: Maximum number of records to return (max 100)

Example:
```bash
GET /students/?offset=0&limit=50
GET /professors/?offset=10&limit=20
GET /courses/?offset=0&limit=100
```
---

### Logs
```bash
# View Docker logs
docker-compose logs
docker-compose logs backend
docker-compose logs nginx
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.