from flask import Flask
from .extensions import db, jwt, cors, celery_init_app
from .models import User
from werkzeug.security import generate_password_hash

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app) # Defaults to "*" for all routes
    
    # Initialize Celery
    app.config.from_mapping(
        CELERY=dict(
            broker_url=app.config['CELERY_BROKER_URL'],
            result_backend=app.config['CELERY_RESULT_BACKEND'],
            task_ignore_result=True,
        ),
    )
    celery_init_app(app)

    # Import and register blueprints
    from .api.auth import auth_bp
    from .api.admin import admin_bp
    from .api.doctor import doctor_bp
    from .api.patient import patient_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    with app.app_context():
        db.create_all()
        create_admin_if_not_exists()

    return app

def create_admin_if_not_exists():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        print("Creating default admin user...")
        hashed_pw = generate_password_hash('admin123')
        admin = User(
            email='admin@hms.com',
            password_hash=hashed_pw,
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@hms.com / admin123")
