from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'

# Initialiser la base de données
init_db()

@app.route('/')
def index():
    db = get_db()
    tasks = db.execute('''
        SELECT * FROM tasks 
        ORDER BY 
            CASE WHEN status = "pending" THEN 1 ELSE 2 END,
            created_at DESC
    ''').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        if title:
            db = get_db()
            db.execute(
                'INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)',
                (title, description, 'pending')
            )
            db.commit()
            return redirect(url_for('index'))
    
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    db = get_db()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        
        db.execute(
            'UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?',
            (title, description, status, task_id)
        )
        db.commit()
        return redirect(url_for('index'))
    
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    db = get_db()
    db.execute('UPDATE tasks SET status = "completed" WHERE id = ?', (task_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)