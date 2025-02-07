from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import db, login_manager  # Importar db y login_manager desde extensions.py
from .models import User  # Importar el modelo de usuario
from flask_login import LoginManager
from .utils import extract_youtube_id

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///morphy.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar db y login_manager
    db.init_app(app)
    login_manager.init_app(app)

    # Cargar el usuario para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.courses import courses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(courses_bp)

    # Configuración Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'  # Ruta al archivo JSON de Swagger (lo puedes generar más tarde)
    
    # Agregar Swagger UI Blueprint
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Flask API"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Agregar el filtro a Jinja
    app.jinja_env.filters['youtube_id'] = extract_youtube_id

    return app
