from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
courses_bp = Blueprint('courses', __name__)

from . import auth, admin, courses