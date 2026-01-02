from .extensions import db
from datetime import datetime
import json

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'doctor', 'patient'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False, cascade="all, delete-orphan")
    patient_profile = db.relationship('Patient', backref='user', uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active
        }

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    doctors = db.relationship('Doctor', backref='department', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True) # made nullable for admin creation flow
    experience_years = db.Column(db.Integer)
    is_verified = db.Column(db.Boolean, default=True)
    contact_info = db.Column(db.String(100))
    
    # Store availability as JSON string simpler than a separate table for now
    # Format: {"Monday": ["09:00", "17:00"], ...}
    availability_schedule = db.Column(db.Text, default='{}') 

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def to_dict(self):
        dept_name = self.department.name if self.department else None
        return {
            'id': self.id,
            'name': self.name,
            'specialization': dept_name,
            'specialization_id': self.specialization_id,
            'experience_years': self.experience_years,
            'is_verified': self.is_verified,
            'contact_info': self.contact_info,
            'availability_schedule': json.loads(self.availability_schedule) if self.availability_schedule else {}
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date)
    contact_info = db.Column(db.String(100))
    address = db.Column(db.String(200))
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': self.dob.isoformat() if self.dob else None,
            'contact_info': self.contact_info,
            'address': self.address
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='booked') # booked, completed, cancelled
    
    # Treatment details (one-to-one with appointment mostly)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name,
            'date_time': self.date_time.isoformat(),
            'status': self.status,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'notes': self.notes
        }
