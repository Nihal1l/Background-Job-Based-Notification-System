# Background Job Based Notification System

A scalable backend notification scheduling system built using Django, Django REST Framework, PostgreSQL, Celery, Redis, and Docker.

The system allows authenticated users to create scheduled notifications that are processed asynchronously using Celery workers and Redis queues.

---

# Features

* JWT Authentication
* User Registration & Login
* Create Scheduled Notifications
* Notification History API
* Background Job Processing
* Celery Worker Integration
* Redis Queue Broker
* Retry Failed Notifications
* Automatic Retry Logic
* Permanent Failure Protection
* Celery Beat Scheduler
* API Security & Permissions
* Swagger/OpenAPI Documentation
* Dockerized Environment
* PostgreSQL Database
* Logging & Monitoring Ready
* Pagination & Filtering
* Production-Oriented Architecture

---

# Tech Stack

| Technology            | Purpose                    |
| --------------------- | -------------------------- |
| Python                | Programming Language       |
| Django                | Backend Framework          |
| Django REST Framework | REST API Development       |
| PostgreSQL            | Primary Database           |
| Redis                 | Message Broker             |
| Celery                | Background Task Queue      |
| Celery Beat           | Scheduled Task Scheduler   |
| Docker                | Containerization           |
| Docker Compose        | Multi-container Management |
| JWT                   | Authentication             |

---

# System Architecture

```text id="s4m8q2"
Client
   ↓
Django REST API
   ↓
JWT Authentication
   ↓
PostgreSQL Database
   ↓
Celery Beat Scheduler
   ↓
Redis Queue Broker
   ↓
Celery Workers
   ↓
Background Notification Processing
```

---

# Project Structure

```text id="m6p1k8"
notification_system/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── __init__.py
│
├── notifications/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   ├── urls.py
│   └── migrations/
│
├── users/
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
├── manage.py
└── README.md
```

---

# Notification Lifecycle

```text id="t9m2q5"
PENDING
   ↓
PROCESSING
   ↓
SENT
```

If failure occurs:

```text id="r3k7m1"
FAILED
   ↓
Retry
   ↓
PERMANENTLY_FAILED
```

Maximum retry limit:

```text id="h5m8q4"
3 retries
```

---

# Setup Instructions

## 1. Clone Repository

```bash id="f2n7k9"
git clone <your-github-repo-url>
cd notification_system
```

---

# 2. Create Environment File

Create:

```text id="w8m3p1"
.env
```

Add:

```env id="y4k9m6"
DEBUG=True

SECRET_KEY=super-secret-key

DB_NAME=notification_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0
```

---

# 3. Build and Start Containers

```bash id="c7p2m5"
docker-compose up --build
```

---

# 4. Run Database Migrations

```bash id="u9m4k2"
docker-compose run web python manage.py migrate
```

---

# 5. Create Superuser (Optional)

```bash id="n1q8m7"
docker-compose run web python manage.py createsuperuser
```

---

# 6. Start Application

```bash id="p5m2k8"
docker-compose up
```

---

# Docker Services

| Service     | Purpose          |
| ----------- | ---------------- |
| web         | Django API       |
| db          | PostgreSQL       |
| redis       | Redis Broker     |
| celery      | Celery Worker    |
| celery-beat | Celery Scheduler |

---

# API Documentation

Swagger/OpenAPI:

```text id="z8m1q6"
http://localhost:8000/api/docs/
```

---

# Authentication APIs

## Register User

POST:

```text id="d4k7m9"
/api/auth/register/
```

Request Body:

```json id="g2m8p4"
{
  "username": "neel",
  "email": "neel@example.com",
  "password": "test1234"
}
```

---

# Login User

POST:

```text id="x7p1m3"
/api/auth/login/
```

Request Body:

```json id="t4m9k5"
{
  "username": "neel",
  "password": "test1234"
}
```

Response:

```json id="b6m2q8"
{
  "refresh": "REFRESH_TOKEN",
  "access": "ACCESS_TOKEN"
}
```

---

# Refresh Access Token

POST:

```text id="j8m4p2"
/api/auth/refresh/
```

Request Body:

```json id="k5q9m1"
{
  "refresh": "REFRESH_TOKEN"
}
```

---

# Notification APIs

## Create Notification

POST:

```text id="s2m7k4"
/api/notifications/create/
```

Headers:

```text id="v8m1q9"
Authorization: Bearer ACCESS_TOKEN
```

Request Body:

```json id="q3m5p8"
{
  "title": "Meeting Reminder",
  "message": "Join meeting at 6 PM",
  "scheduled_time": "2026-06-10T18:00:00Z"
}
```

---

# Get Notification History

GET:

```text id="m4q8p1"
/api/notifications/
```

Optional Filtering:

```text id="r7m2k5"
/api/notifications/?status=FAILED
```

---

# Retry Failed Notification

POST:

```text id="t5m9q3"
/api/notifications/<id>/retry/
```

---

# Health Check API

GET:

```text id="y1m6k8"
/api/notifications/health/
```

Response:

```json id="u4p9m2"
{
  "status": "healthy"
}
```

---

# Retry Logic

* Failed notifications automatically retry
* Maximum retry limit is 3
* After 3 failures:

```text id="h9m2q7"
PERMANENTLY_FAILED
```

* Infinite retry loops are prevented

---

# Background Processing Flow

```text id="k7m4p9"
User Creates Notification
          ↓
Stored in PostgreSQL
          ↓
Celery Beat Checks Schedule
          ↓
Due Notifications Sent to Redis Queue
          ↓
Celery Worker Processes Task
          ↓
Notification Status Updated
```

---

# Security Features

* JWT Authentication
* Protected APIs
* User Ownership Validation
* API Throttling
* Retry Restrictions
* Input Validation
* Secure Password Hashing

---

# Database Optimizations

* Indexed fields:

  * status
  * scheduled_time
* Query filtering
* Pagination support
* Race-condition prevention using `select_for_update()`

---

# Logging

The system includes logging support for:

* Task processing
* Failed jobs
* Retry attempts
* Error tracking

---

# Edge Cases Handled

* Scheduled time in the past
* Infinite retry prevention
* Duplicate processing prevention
* Unauthorized access
* Invalid JWT tokens
* Retry limit exceeded
* Race conditions

---

# Future Improvements

Possible future enhancements:

* Email/SMS notification delivery
* RabbitMQ integration
* Kubernetes deployment
* Prometheus & Grafana monitoring
* WebSocket real-time updates
* Multiple notification channels
* Notification templates
* Distributed Celery workers

---

# Author

Developed as a backend engineering task focused on:

* Scalable architecture
* Queue-based systems
* Background processing
* Distributed task handling
* Production-ready API design
