from flask import Blueprint, request, jsonify
from app.models import User, Patient, db
from app.extensions import jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Only Patients register themselves
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    # Optional fields
    dob = data.get('dob') # 'YYYY-MM-DD'
    contact_info = data.get('contact_info')
    address = data.get('address')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_pw = generate_password_hash(password)
    
    new_user = User(email=email, password_hash=hashed_pw, role='patient')
    db.session.add(new_user)
    db.session.flush() # get id

    new_patient = Patient(
        id=new_user.id,
        name=name,
        contact_info=contact_info,
        address=address
    )
    if dob:
        try:
            new_patient.dob = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            pass # Handle error or ignore

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    if not user.is_active:
         return jsonify({'error': 'Account is disabled'}), 403

    # specific details based on role
    additional_claims = {'role': user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    
    user_data = user.to_dict()
    if user.role == "patient" and user.patient_profile:
        user_data.update(user.patient_profile.to_dict())
    elif user.role == "doctor" and user.doctor_profile:
        user_data.update(user.doctor_profile.to_dict())

    return jsonify({
        'token': access_token,
        'user': user_data
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    user_data = user.to_dict()
    if user.role == "patient" and user.patient_profile:
        user_data.update(user.patient_profile.to_dict())
    elif user.role == "doctor" and user.doctor_profile:
        user_data.update(user.doctor_profile.to_dict())
        
    return jsonify(user_data), 200
