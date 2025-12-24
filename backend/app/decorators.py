from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User
from flask import jsonify

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role != required_role:
                 return jsonify({'error': 'Admins only!' if required_role == 'admin' else 'Unauthorized'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def admin_required(fn):
    return role_required('admin')(fn)

def doctor_required(fn):
    return role_required('doctor')(fn)

def patient_required(fn):
    return role_required('patient')(fn)
