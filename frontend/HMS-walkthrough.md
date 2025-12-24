# Hospital Management System - Implementation Plan

## Goal
Build a comprehensive Hospital Management System (HMS) with role-based access for Admins, Doctors, and Patients. The system will handle appointments, patient history, and background jobs for reminders and reports.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** VueJS 3 (Vite) + Bootstrap 5
- **Database:** SQLite (SQLAlchemy ORM)
- **Caching & Messaging:** Redis
- **Background Jobs:** Celery
- **Authentication:** Flask-JWT-Extended or Session based

## User Review Required
> [!IMPORTANT]
> - The application relies on **Redis** being available on the local machine for Caching and Celery jobs.
> - **SQLite** database will be created programmatically on the first run.

## Proposed Architecture

### Directory Structure
```
/
├── backend/
│   ├── app/
│   │   ├── __init__.py      # App factory
│   │   ├── models.py        # Database models
│   │   ├── api/             # API Blueprints
│   │   ├── tasks.py         # Celery tasks
│   │   ├── auth.py          # Authentication logic
│   ├── config.py
│   ├── run.py
│   ├── requirements.txt
├── frontend/                # VueJS Application
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── store/           # State management
│   │   ├── router/
│   │   ├── App.vue
│   │   ├── main.js
│   ├── index.html
│   ├── vite.config.js
```

### Database Schema (SQLite via SQLAlchemy)

#### Users Table (Polymorphic or Single Table with Role)
*Since requirements specify distinct attributes, a base User model with specific tables or effective role management is needed. Given the simplicity, a Role-based single table or linked tables works.*

1.  **User**
    -   `id` (PK)
    -   `email` (Unique)
    -   `password_hash`
    -   `role` (Enum: 'admin', 'doctor', 'patient')
    -   `is_active`
    -   `details` (Relationship to specific profiles)

2.  **Doctor**
    -   `id` (PK, FK to User.id)
    -   `name`
    -   `specialization_id` (FK)
    -   `experience_years`
    -   `is_available` (Boolean)
    -   `availability_schedule` (JSON/String - Next 7 days)

3.  **Patient**
    -   `id` (PK, FK to User.id)
    -   `name`
    -   `dob`
    -   `contact_info`
    -   `address`

4.  **Admin**
    -   `id` (PK, FK to User.id)
    -   `name`

5.  **Department / Specialization**
    -   `id` (PK)
    -   `name`
    -   `description`

6.  **Appointment**
    -   `id` (PK)
    -   `patient_id` (FK)
    -   `doctor_id` (FK)
    -   `date_time` (DateTime)
    -   `status` (Enum: 'booked', 'completed', 'cancelled')

7.  **Treatment**
    -   `id` (PK)
    -   `appointment_id` (FK)
    -   `diagnosis`
    -   `prescription`
    -   `notes`

### API Endpoints
-   **Auth:** `/api/login`, `/api/register`
-   **Admin:**
    -   `POST /api/admin/doctors` (Add doctor)
    -   `DELETE /api/admin/doctors/:id`
    -   `GET /api/admin/stats` (Dashboard stats)
-   **Doctor:**
    -   `GET /api/doctor/appointments`
    -   `POST /api/doctor/appointments/:id/complete` (Add treatment)
-   **Patient:**
    -   `GET /api/doctors` (Search/Filter)
    -   `POST /api/appointments` (Book)
    -   `GET /api/patient/history`

### Background Jobs (Celery)
1.  **Daily Reminder:** Cron job at 8:00 AM. Checks appointments for today -> Sends Email/SMS (Mock print/log).
2.  **Monthly Report:** Cron job 1st of month. Aggregates stats -> Sends HTML Email (Mock).
3.  **CSV Export:** User triggered. Generates CSV -> Returns path/content.

## Verification Plan
### Automated Tests
-   **Backend:** Pytest for API endpoints (auth, booking logic).
-   **Jobs:** Trigger Celery tasks manually and verify output/logs.

### Manual Verification
-   Admin Login -> Add Doctor -> Verify in DB.
-   Patient Login -> Book Appointment -> Check Doctor View.
-   Doctor Login -> Complete Appointment -> Check Patient History.
-   Redis Caching -> Check headers or logs for cache hits.
