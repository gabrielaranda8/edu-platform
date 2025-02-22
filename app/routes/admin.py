# admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User
from ..extensions import db

# Definir el Blueprint
admin_bp = Blueprint('admin', __name__)

# Definir las rutas
@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('auth.login'))
    return render_template('admin.html')

@admin_bp.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash("No tienes permisos para realizar esta acción.", "error")
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"Usuario '{user.username}' eliminado exitosamente.", "success")
    else:
        flash("Usuario no encontrado.", "error")
    return redirect(url_for('admin.dashboard_users'))

# Ruta del dashboard_users
@admin_bp.route('/admin/dashboard_users', methods=['GET', 'POST'])
@login_required
def dashboard_users():
    if current_user.role != 'admin':
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if not username or not password or not role:
            flash("Todos los campos son obligatorios.", "error")
        elif User.query.filter_by(username=username).first():
            flash("El usuario ya existe.", "error")
        else:
            user = User(username=username, role=role)
            user.set_password(password)  # Asegúrate de que esta función está bien definida
            db.session.add(user)
            db.session.commit()
            flash(f"Usuario '{username}' creado exitosamente con rol '{role}'.", "success")

    users = User.query.all()
    return render_template('dashboard_users.html', users=users)

# Importar los módulos aquí, después de haber definido el Blueprint
from . import auth, courses
