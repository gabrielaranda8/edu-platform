# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from ..models import User
from ..extensions import db

# Definir el Blueprint
auth_bp = Blueprint('auth', __name__)

# Definir las rutas
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Has iniciado sesión correctamente.", "success")
            if user.role == 'admin':
                return redirect(url_for('admin.admin'))
            elif user.role == 'gestion':
                return redirect(url_for('courses.gestion'))
            else:
                return redirect(url_for('courses.cursos'))
        else:
            flash("Usuario o contraseña incorrectos. Intenta de nuevo.", "error")
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for('auth.login'))

# Importar los módulos aquí, después de haber definido el Blueprint
from . import admin, courses