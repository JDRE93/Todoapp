from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime  
from flask_migrate import Migrate 
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user, logout_user



load_dotenv()


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = '630531736e0d224c8026fce4eda78a23'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id = db.Column(db.Integer, primary_key = True)
    completada = db.Column(db.Boolean, nullable = False, default = False)
    tarea = db.Column(db.Text, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, nullable = True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, nullable = False, unique = True)
    password_hash = db.Column(db.Text, nullable = False)

@app.route('/')
@login_required
def pagina_de_inicio():
   
    task_desde_db = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all()

    
    return render_template('index.html', tasks=task_desde_db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        tarea = request.form['tarea']
        fecha_vencimiento_texto = request.form['fecha_vencimiento']
        fecha_vencimiento_obj = None
        if fecha_vencimiento_texto:
            fecha_vencimiento_obj = datetime.strptime(fecha_vencimiento_texto, '%Y-%m-%d')

        nueva_tarea = Task(
            tarea= tarea,
            fecha_vencimiento = fecha_vencimiento_obj,
            user_id=current_user.id
        )

        db.session.add(nueva_tarea)
        db.session.commit()

        return redirect(url_for('pagina_de_inicio'))
    
    return render_template('create.html')

@app.route('/update/<int:task_id>', methods=['POST'])
@login_required  # <-- Añade protección a esta ruta también
def update_task(task_id):
    # Busca la tarea por su ID Y que le pertenezca al usuario actual
    task_a_actualizar = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    task_a_actualizar.completada = not task_a_actualizar.completada
    db.session.commit()
    
    return redirect(url_for('pagina_de_inicio'))

@app.route('/register', methods= ['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        usuario = request.form['username']
        contraseña = request.form['password']
        hashed_password = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        new_user = User(
            username = usuario,
            password_hash = hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('pagina_de_inicio'))
    
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contraseña = request.form['password']
        usuario_consulta = User.query.filter_by(username = usuario).first()

        if usuario_consulta != None and bcrypt.check_password_hash(usuario_consulta.password_hash, contraseña):
            login_user(usuario_consulta)
            return redirect(url_for('pagina_de_inicio'))
        else:
            pass
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))