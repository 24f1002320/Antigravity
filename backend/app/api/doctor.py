from flask import Blueprint, request, jsonify
from app.models import Appointment, Doctor, Patient, db
from app.decorators import doctor_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
import json

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/appointments', methods=['GET'])
@doctor_required
def get_appointments():
    doctor_id = get_jwt_identity()
    # Filter by date/upcoming
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).order_by(Appointment.date_time).all()
    return jsonify([a.to_dict() for a in appointments])

@doctor_bp.route('/appointments/<int:id>/complete', methods=['POST'])
@doctor_required
def complete_appointment(id):
    doctor_id = get_jwt_identity()
    appointment = Appointment.query.filter_by(id=id, doctor_id=doctor_id).first()
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    
    data = request.get_json()
    appointment.diagnosis = data.get('diagnosis')
    appointment.prescription = data.get('prescription')
    appointment.notes = data.get('notes')
    appointment.status = 'completed'
    
    db.session.commit()
    return jsonify({'message': 'Appointment completed'}), 200

@doctor_bp.route('/availability', methods=['GET', 'PUT'])
@doctor_required
def manage_availability():
    doctor_id = get_jwt_identity()
    doctor = Doctor.query.get(doctor_id)
    
    if request.method == 'GET':
         return jsonify(json.loads(doctor.availability_schedule) if doctor.availability_schedule else {})
         
    data = request.get_json() # expects dict {"YYYY-MM-DD": ["09:00", ...]} or {"Monday": ...}
    # Requirement: availability for next 7 days.
    # We'll store it as is for now.
    doctor.availability_schedule = json.dumps(data)
    db.session.commit()
    return jsonify({'message': 'Availability updated'}), 200
