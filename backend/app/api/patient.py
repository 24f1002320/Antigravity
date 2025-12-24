from flask import Blueprint, request, jsonify
from app.models import Doctor, Appointment, Department, db
from app.decorators import patient_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/doctors', methods=['GET'])
@patient_required
def search_doctors():
    specialization_id = request.args.get('specialization_id')
    doctors_query = Doctor.query
    if specialization_id:
        doctors_query = doctors_query.filter_by(specialization_id=specialization_id)
    
    doctors = doctors_query.all()
    return jsonify([d.to_dict() for d in doctors])

@patient_bp.route('/departments', methods=['GET'])
@patient_required
def get_departments():
    depts = Department.query.all()
    return jsonify([d.to_dict() for d in depts])

@patient_bp.route('/appointments', methods=['POST'])
@patient_required
def book_appointment():
    patient_id = get_jwt_identity()
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    date_str = data.get('date_time') # ISO format
    
    try:
        date_time = datetime.fromisoformat(date_str)
    except ValueError:
         return jsonify({'error': 'Invalid date format'}), 400
         
    # Check availability/conflict
    existing = Appointment.query.filter_by(doctor_id=doctor_id, date_time=date_time).filter(Appointment.status != 'cancelled').first()
    if existing:
        return jsonify({'error': 'Slot already booked'}), 409
        
    new_appt = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        date_time=date_time,
        status='booked'
    )
    db.session.add(new_appt)
    db.session.commit()
    return jsonify({'message': 'Appointment booked'}), 201

@patient_bp.route('/appointments/<int:id>', methods=['PUT', 'DELETE'])
@patient_required
def manage_appointment(id):
    patient_id = get_jwt_identity()
    appt = Appointment.query.filter_by(id=id, patient_id=patient_id).first()
    
    if not appt:
        return jsonify({'error': 'Appointment not found'}), 404
        
    if request.method == 'DELETE' or (request.method == 'PUT' and request.json.get('status') == 'cancelled'):
        appt.status = 'cancelled'
        db.session.commit()
        return jsonify({'message': 'Appointment cancelled'}), 200
        
    # Reschedule
    if request.method == 'PUT':
        new_date_str = request.json.get('date_time')
        if new_date_str:
            new_date = datetime.fromisoformat(new_date_str)
            # Check conflict
            if Appointment.query.filter_by(doctor_id=appt.doctor_id, date_time=new_date).filter(Appointment.status != 'cancelled').first():
                 return jsonify({'error': 'Slot unavailable'}), 409
            appt.date_time = new_date
            db.session.commit()
            return jsonify({'message': 'Appointment rescheduled'}), 200

    return jsonify({'error': 'Invalid action'}), 400

@patient_bp.route('/history', methods=['GET'])
@patient_required
def get_history():
    patient_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.date_time.desc()).all()
    return jsonify([a.to_dict() for a in appointments])

@patient_bp.route('/export', methods=['POST'])
@patient_required
def export_history():
    from app.tasks import export_patient_history
    user_id = get_jwt_identity()
    export_patient_history.delay(user_id)
    return jsonify({'message': 'Export started. You will be notified when ready.'}), 202
