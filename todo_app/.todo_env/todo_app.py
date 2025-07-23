from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'mysecretkey' # Секретный ключ для сессий
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' #Доступ к базе данных SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Отключаем отслеживание изменений для производительности

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now()) 
    
    def __repr__(self):
        return f'<Task {self.id}'
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])    
def index():
    tasks = Task.query.order_by(Task.date_created.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['content']
    if not task_content:
        flash('Task content cannot be empty!', 'error')
        return redirect(url_for('index'))

    new_task = Task(content=task_content)
    try:
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding task: {str(e)}', 'error')
        
    return redirect(url_for('index'))
    
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting task', 'error')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)