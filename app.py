from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///morphy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Curso
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lessons = db.relationship('Lesson', backref='course', cascade="all, delete-orphan", lazy=True)

# Modelo de Lección
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)


# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta de administración
@app.route('/admin', methods=['GET', 'POST'])
# @login_required
def admin():
    if request.method == 'POST':
        # Crear un nuevo usuario
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("El usuario ya existe.", "error")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash(f"Usuario '{username}' creado exitosamente.", "success")

    # Obtener todos los usuarios
    users = User.query.all()
    return render_template('admin.html', users=users)

# Ruta para borrar un usuario
@app.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"Usuario '{user.username}' eliminado exitosamente.", "success")
    else:
        flash("Usuario no encontrado.", "error")
    return redirect(url_for('admin'))

# Rutas de la aplicación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Has iniciado sesión correctamente.", "success")
            return redirect(url_for('gestion'))
        else:
            flash("Usuario o contraseña incorrectos. Intenta de nuevo.", "error")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for('login'))

@app.route('/create_course', methods=['POST'])
@login_required
def create_course():
    title = request.form['title']
    description = request.form['description']
    new_course = Course(title=title, description=description)
    db.session.add(new_course)
    db.session.commit()
    flash(f"Curso '{title}' creado exitosamente.", "success")
    return redirect(url_for('gestion'))

@app.route('/add_lesson/<int:course_id>', methods=['POST'])
@login_required
def add_lesson(course_id):
    title = request.form['title']
    content = request.form['content']
    new_lesson = Lesson(title=title, content=content, course_id=course_id)
    db.session.add(new_lesson)
    db.session.commit()
    flash(f"Lección '{title}' agregada exitosamente.", "success")
    return redirect(url_for('gestion'))

@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
        flash(f"Curso '{course.title}' eliminado exitosamente.", "success")
    else:
        flash("Curso no encontrado.", "error")
    return redirect(url_for('gestion'))

@app.route('/gestion')
@login_required
def gestion():
    courses = Course.query.all()
    return render_template('gestion.html', courses=courses)

# Crear la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)