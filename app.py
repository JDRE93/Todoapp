from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime  
from flask_migrate import Migrate 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Josdaro739.@localhost:5432/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    completada = db.Column(db.Boolean, nullable = False, default = False)
    tarea = db.Column(db.Text, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, nullable = True)

@app.route('/')
def pagina_de_inicio():
   
    task_desde_db = Task.query.order_by(Task.id.desc()).all()

    
    return render_template('index.html', tasks=task_desde_db)

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
            fecha_vencimiento = fecha_vencimiento_obj
        )

        db.session.add(nueva_tarea)
        db.session.commit()

        return redirect(url_for('pagina_de_inicio'))
    
    return render_template('create.html')

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task_a_actualizar = Task.query.get(task_id)
    task_a_actualizar.completada = not task_a_actualizar.completada
    db.session.commit()
    
    return redirect(url_for('pagina_de_inicio'))