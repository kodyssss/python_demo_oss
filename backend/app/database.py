import mysql.connector
from .config import Config
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    for attempt in range(5):
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB
            )
            return conn
        except mysql.connector.Error as err:
            logger.error(f"Connection attempt {attempt + 1} failed: {err}")
            time.sleep(2)
    raise Exception("Failed to connect to MySQL after multiple attempts")

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Check if avatar_url column exists
        cursor.execute("SHOW COLUMNS FROM users LIKE 'avatar_url'")
        if not cursor.fetchone():
            # Add avatar_url column
            cursor.execute('ALTER TABLE users ADD COLUMN avatar_url VARCHAR(512)')
            logger.info("Added avatar_url column to users table")
        conn.commit()
        logger.info("Users table initialized")
    except mysql.connector.Error as err:
        logger.error(f"Error initializing database: {err}")
        raise
    finally:
        cursor.close()
        conn.close()

def insert_name(name, avatar_url=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, avatar_url) VALUES (%s, %s)', (name, avatar_url))
        conn.commit()
    except mysql.connector.Error as err:
        logger.error(f"Error inserting name: {err}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_all_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT name, created_at, avatar_url FROM users ORDER BY created_at DESC')
        names = cursor.fetchall()
        return names
    except mysql.connector.Error as err:
        logger.error(f"Error fetching names: {err}")
        raise
    finally:
        cursor.close()
        conn.close()