import mysql.connector
import os

# --- MariaDB/MySQL Connection Details ---
DB_CONFIG = {
    'host': '192.168.56.104',
    'user': 'meda', 
    'password': '0000',
    'database': 'task'
}
# ------------------------------------------


def get_db():
    # 2. Changed connection method
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        # Use buffered cursor to fetch rows, similar to how sqlite3 works
        # You might use cursor=db.cursor(dictionary=True) for dict-like rows
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to MariaDB: {err}")
        # Re-raise the error or handle it as appropriate for your application
        raise

def init_db():
    # We no longer check for file existence (os.path.exists), 
    # as the database might not be initialized yet on the remote server.
    db = get_db()
    cursor = db.cursor() # MariaDB requires a cursor to execute commands

    # 3. Changed CREATE TABLE syntax for MariaDB/MySQL
    # Note: AUTOINCREMENT is replaced by AUTO_INCREMENT, and we use VARCHAR for text.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --- Sample Data ---
    # MariaDB/MySQL uses %s as the parameter placeholder by default
    cursor.execute(
        "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)",
        ("Exemple de tâche", "Ceci est une tâche d'exemple", "pending")
    )

    db.commit()
    cursor.close()
    db.close()

# Example usage to initialize the database:
# init_db()

