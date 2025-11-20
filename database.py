import mysql.connector
import os

# --- MariaDB/MySQL Connection Details ---
DB_CONFIG = {
    'host': '172.31.73.182',
    'user': 'meda', 
    'password': '0000',
    'database': 'task'
}
# ------------------------------------------


def get_db():
    # 2. Changed connection method
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to MariaDB: {err}")
        raise

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    db.commit()
    cursor.close()
    db.close()


