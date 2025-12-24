# Hospital Management System - Walkthrough

## Overview
The Hospital Management System is a full-stack web application built with Flask (Backend) and VueJS (Frontend). It supports three roles: Admin, Doctor, and Patient, with features for appointment booking, medical history management, and automated background jobs.

## Architecture
- **Backend**: Flask API with SQLAlchemy (SQLite), Flask-JWT-Extended (Auth), Celery (Background Jobs).
- **Frontend**: VueJS 3 with Vite, Pinia (Store), Vue Router, and Bootstrap 5.
- **Background Jobs**: Redis-backed Celery workers for daily reminders and reports.

## Features Implemented
### Admin
- **Dashboard**: View statistics (Doctors, Patients, Appointments).
- **Doctors**: Add, delete, and view doctors. Manage Departments.
- **Appointments**: View all appointments system-wide.

### Doctor
- **Dashboard**: View assigned appointments.
- **Treatments**: Mark appointments as complete, add diagnosis, prescription, and notes.
- **Availability**: Update weekly availability schedule.

### Patient
- **Registration**: Self-registration for new patients.
- **Booking**: Search doctors by department and book appointments.
- **History**: View past appointments and download treatment history (CSV).

## Setup & Running

### Prerequisites
- Python 3.8+
- Node.js 16+
- Redis Server (must be running)

### 1. Start Backend (Terminal 1)
```bash
cd backend
python3 -m pip install -r requirements.txt
python3 run.py
```
*Note: The database `hms.db` and default Admin user (`admin@hms.com`/`admin123`) are created automatically on first run.*

### 2. Start Celery Worker & Beat (Terminal 2)
```bash
cd backend
python3 -m celery -A make_celery.celery_app worker --loglevel=info &
python3 -m celery -A make_celery.celery_app beat --loglevel=info &
```

### 3. Start Frontend (Terminal 3)
```bash
cd frontend
npm install
npm run dev
```
Access the application at `http://localhost:5173`.

## Verification Results
We verified the core flows using a browser agent:
- **Admin**: Successfully logged in, created a "Cardiology" department, and added "Dr. Heart".
- **API**: Verified endpoints for auth, admin management, and data retrieval.
- **Exports**: CSV export triggered via Celery task.

## Project Structure
```
/
├── backend/
│   ├── app/ (Models, API routes, Tasks)
│   ├── run.py (Entry point)
│   └── make_celery.py (Worker entry)
├── frontend/
│   ├── src/ (Views, Components, Store)
│   └── vite.config.js
```
