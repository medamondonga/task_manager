from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db
from datetime import datetime

app = Flask(__name__)

# Initialiser la base de données
init_db()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
        SELECT * FROM tasks 
        ORDER BY 
            CASE WHEN status = 'pending' THEN 1 ELSE 2 END,
            created_at DESC
    ''')
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        if title:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)',
                (title, description, 'pending')
            )
            db.commit()
            return redirect(url_for('index'))
    
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        
        cursor.execute(
            'UPDATE tasks SET title = %s, description = %s, status = %s WHERE id = %s',
            (title, description, status, task_id)
        )
        db.commit()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
    task = cursor.fetchone()
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE tasks SET status = "completed" WHERE id = %s', (task_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)