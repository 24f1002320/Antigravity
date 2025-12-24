from flask import Blueprint, request, jsonify
from app.models import User, Doctor, Patient, Appointment, Department, db
from app.decorators import admin_required
from werkzeug.security import generate_password_hash
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    doctor_count = Doctor.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    return jsonify({
        'doctors': doctor_count,
        'patients': patient_count,
        'appointments': appointment_count
    })

@admin_bp.route('/doctors', methods=['GET'])
@admin_required
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([d.to_dict() for d in doctors])

@admin_bp.route('/doctors', methods=['POST'])
@admin_required
def add_doctor():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    specialization_id = data.get('specialization_id')
    experience = data.get('experience_years')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password_hash=hashed_pw, role='doctor')
    db.session.add(new_user)
    db.session.flush()

    new_doctor = Doctor(
        id=new_user.id,
        name=name,
        specialization_id=specialization_id,
        experience_years=experience,
        availability_schedule=json.dumps({}) # Initialize empty
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor added successfully'}), 201

@admin_bp.route('/doctors/<int:id>', methods=['DELETE'])
@admin_required
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    # We should also delete the user or mark inactive
    user = User.query.get(id) # User id same as doctor id
    if user:
        db.session.delete(user) # Cascade deletes doctor
        db.session.commit()
    return jsonify({'message': 'Doctor removed'}), 200

@admin_bp.route('/patients', methods=['GET'])
@admin_required
def get_patients():
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients])

@admin_bp.route('/appointments', methods=['GET'])
@admin_required
def get_appointments():
    appointments = Appointment.query.order_by(Appointment.date_time.desc()).all()
    return jsonify([a.to_dict() for a in appointments])

@admin_bp.route('/departments', methods=['GET', 'POST'])
@admin_required
def manage_departments():
    if request.method == 'GET':
        depts = Department.query.all()
        return jsonify([d.to_dict() for d in depts])
    
    data = request.get_json()
    new_dept = Department(name=data.get('name'), description=data.get('description'))
    db.session.add(new_dept)
    db.session.commit()
    return jsonify(new_dept.to_dict()), 201
