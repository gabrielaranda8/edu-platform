# courses.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Course, Lesson
from ..extensions import db

# Definir el Blueprint
courses_bp = Blueprint('courses', __name__)

# Definir las rutas
@courses_bp.route('/cursos')
@login_required
def cursos():
    courses = Course.query.all()
    return render_template('cursos.html', courses=courses)

@courses_bp.route('/gestion')
@login_required
def gestion():
    if current_user.role not in ['admin', 'gestion']:
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('auth.login'))
    courses = Course.query.all()
    return render_template('gestion.html', courses=courses)

@courses_bp.route('/create_course', methods=['POST'])
@login_required
def create_course():
    title = request.form['title']
    description = request.form['description']
    image_url = request.form['image_url']
    new_course = Course(title=title, description=description, image_url=image_url)
    db.session.add(new_course)
    db.session.commit()
    flash(f"Curso '{title}' creado exitosamente.", "success")
    return redirect(url_for('courses.gestion'))

@courses_bp.route('/add_lesson/<int:course_id>', methods=['POST'])
@login_required
def add_lesson(course_id):
    title = request.form['title']
    content = request.form['content']
    new_lesson = Lesson(title=title, content=content, course_id=course_id)
    db.session.add(new_lesson)
    db.session.commit()
    flash(f"Lección '{title}' agregada exitosamente.", "success")
    return redirect(url_for('courses.gestion'))

@courses_bp.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
        flash(f"Curso '{course.title}' eliminado exitosamente.", "success")
    else:
        flash("Curso no encontrado.", "error")
    return redirect(url_for('courses.gestion'))

# Importar los módulos aquí, después de haber definido el Blueprint
from . import auth, admin
