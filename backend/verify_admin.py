from app import create_app
from app.models import User
from werkzeug.security import check_password_hash

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@hms.com').first()
    if admin:
        print(f"Admin found: {admin.email}")
        print(f"Role: {admin.role}")
        print(f"Is Active: {admin.is_active}")
        print(f"Password Check ('admin123'): {check_password_hash(admin.password_hash, 'admin123')}")
    else:
        print("Admin user NOT found!")
