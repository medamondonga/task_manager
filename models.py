from database import get_db

class Task:
    def __init__(self, id, title, description, status, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at
    
    @staticmethod
    def get_all():
        db = get_db()
        return db.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    
    @staticmethod
    def get_by_id(task_id):
        db = get_db()
        return db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    @staticmethod
    def create(title, description):
        db = get_db()
        db.execute(
            'INSERT INTO tasks (title, description) VALUES (?, ?)',
            (title, description)
        )
        db.commit()
    
    @staticmethod
    def update(task_id, title, description, status):
        db = get_db()
        db.execute(
            'UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?',
            (title, description, status, task_id)
        )
        db.commit()
    
    @staticmethod
    def delete(task_id):
        db = get_db()
        db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()