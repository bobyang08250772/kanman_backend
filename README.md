
<h1>KanMan</h1>
KanMan is a modern, user-friendly Kanban-style project management tool designed to help teams and individuals organize tasks efficiently. It features role-based access, task assignment, and real-time collaboration for seamless workflow management.

<h2>Features</h2>
Intuitive Kanban board with customizable columns (To-Do, In Progress, Review, Done)

Task creation, editing, and status tracking

User roles: Guest, User, Admin with granular permissions

Task assignment and review workflows

Commenting system for task discussions

Responsive UI for desktop and mobile

Secure backend with Django REST Framework and token-based authentication

<h2>Tech Stack</h2>
Frontend: HTML, CSS, JavaScript (Vanilla or your chosen framework)

Backend: Django & Django REST Framework

Database: SQLite (for development)

Authentication: Django's built-in user system and token auth

# Kanman Django Project 

This guide explains how to set up and run an existing Django project using a `requirements.txt` file.

---

## 📦 Prerequisites

- Python 3.13+
- pip installed
- (Optional but recommended) Python virtual environment (`venv`)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/bobyang08250772/kanman.git
```

### 2. Frontend
Notice Frontend and Backend should be runing seperately.
Go to frontend folder, open index.html in Live Server

### 3. Backend

```bash
cd backend
```

### 3.1. Create and Activate a Virtual Environment
```bash
python -m venv venv
```

####  Activate on macOS/Linux
```bash
source venv/bin/activate
```

####  Activate on Windows
```bash
venv\Scripts\activate
```

### 3.2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.3. Run Migrations
```bash
python manage.py migrate
```

### 3.4. Create a Superuser
```bash
python manage.py createsuperuser
```

### 3.5. Run the Development Server
```bash
python manage.py runserver
```
Open in browser: http://127.0.0.1:8000/

### 3.6. Create Guest User for Guest Login

Log into the admin page of the project and create a guest user with the following information:

| Field       | Value                |
|-------------|----------------------|
| **Username** | guest@guest.de       |
| **Email**    | guest@guest.de       |
| **Password** | ZrfV@7zA7dUBG6R      |
| **First Name** | Guest              |
| **Last Name**  | User               |






