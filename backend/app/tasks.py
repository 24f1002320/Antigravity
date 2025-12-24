from celery import shared_task
from app.models import Appointment, Patient, User, Doctor, db
from app.extensions import celery_app # Not managing beat here usually, but defining tasks
import time
from datetime import datetime, timedelta
import csv
import os

@shared_task(ignore_result=False)
def send_daily_reminders():
    print("Starting daily reminders job...")
    today = datetime.now().date()
    # Find appointments for today
    # Note: Appointment.date_time is DateTime
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    appointments = Appointment.query.filter(
        Appointment.date_time >= start_of_day,
        Appointment.date_time <= end_of_day,
        Appointment.status == 'booked'
    ).all()
    
    count = 0
    for appt in appointments:
        patient = appt.patient
        # Mock sending
        print(f"REMINDER: Dear {patient.name}, you have an appointment with {appt.doctor.name} at {appt.date_time.strftime('%H:%M')}.")
        count += 1
    
    return f"Sent {count} reminders."

@shared_task(ignore_result=False)
def send_monthly_report():
    print("Starting monthly report job...")
    # Logic for last month
    today = datetime.now().date()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    start_date = last_month.replace(day=1)
    end_date = first # strictly less than first of this month
    
    doctors = Doctor.query.all()
    for doc in doctors:
        # Get appts
        appts = Appointment.query.filter(
            Appointment.doctor_id == doc.id,
            Appointment.date_time >= datetime.combine(start_date, datetime.min.time()),
            Appointment.date_time < datetime.combine(end_date, datetime.min.time())
        ).all()
        
        report = f"Monthly Report for Dr. {doc.name}\nMonth: {start_date.strftime('%B %Y')}\nTotal Appointments: {len(appts)}\n"
        print(f"SENDING REPORT TO {doc.user.email}:\n{report}")
        
    return "Monthly reports sent."

@shared_task(ignore_result=False)
def export_patient_history(user_id):
    print(f"Exporting history for user {user_id}...")
    # Use app context ideally handled by shared_task in flask-celery
    user = User.query.get(user_id)
    if not user or user.role != 'patient':
        return "Invalid user"
        
    patient = user.patient_profile
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    
    filename = f"history_{patient.id}_{int(time.time())}.csv"
    filepath = os.path.join(os.getcwd(), 'backend', 'exports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Doctor', 'Diagnosis', 'Prescription', 'Notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for appt in appointments:
            writer.writerow({
                'Date': appt.date_time,
                'Doctor': appt.doctor.name,
                'Diagnosis': appt.diagnosis,
                'Prescription': appt.prescription,
                'Notes': appt.notes
            })
            
    print(f"Export ready at {filepath}")
    # Notify user (Mock)
    print(f"ALERT: Dear {patient.name}, your history export is ready.")
    return filepath
