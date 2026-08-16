import os
import sqlite3
import logging
import re
from config.settings import Config

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track active database type: can be 'snowflake' or 'sqlite'
DB_ENGINE = None

class DatabaseConfigurationError(Exception):
    """Custom exception raised when database configuration or connection fails."""
    pass

def get_snowflake_connection():
    """Attempts to connect to Snowflake using config settings."""
    # Ensure credentials are present
    required_vars = {
        'SNOWFLAKE_ACCOUNT': Config.SNOWFLAKE_ACCOUNT,
        'SNOWFLAKE_USER': Config.SNOWFLAKE_USER,
        'SNOWFLAKE_PASSWORD': Config.SNOWFLAKE_PASSWORD,
        'SNOWFLAKE_WAREHOUSE': Config.SNOWFLAKE_WAREHOUSE,
        'SNOWFLAKE_DATABASE': Config.SNOWFLAKE_DATABASE,
        'SNOWFLAKE_SCHEMA': Config.SNOWFLAKE_SCHEMA,
        'SNOWFLAKE_ROLE': Config.SNOWFLAKE_ROLE
    }
    
    missing_vars = [k for k, v in required_vars.items() if not v]
    if missing_vars:
        error_msg = f"Missing required Snowflake environment variables: {', '.join(missing_vars)}."
        logger.error(error_msg)
        raise DatabaseConfigurationError(error_msg)
        
    try:
        import snowflake.connector
        conn = snowflake.connector.connect(
            user=Config.SNOWFLAKE_USER,
            password=Config.SNOWFLAKE_PASSWORD,
            account=Config.SNOWFLAKE_ACCOUNT,
            warehouse=Config.SNOWFLAKE_WAREHOUSE,
            database=Config.SNOWFLAKE_DATABASE,
            schema=Config.SNOWFLAKE_SCHEMA,
            role=Config.SNOWFLAKE_ROLE
        )
        logger.info("Successfully connected to Snowflake database.")
        return conn
    except ImportError as e:
        error_msg = "snowflake-connector-python package is not installed."
        logger.error(error_msg)
        raise DatabaseConfigurationError(error_msg) from e
    except Exception as e:
        error_msg = f"Failed to connect to Snowflake database: {e}"
        logger.error(error_msg)
        raise DatabaseConfigurationError(error_msg) from e

def get_sqlite_connection():
    """Establishes connection to the local SQLite database."""
    db_dir = os.path.dirname(Config.SQLITE_DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(Config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if running SQLite, or verifies Snowflake connection."""
    global DB_ENGINE
    
    if Config.USE_SQLITE:
        DB_ENGINE = 'sqlite'
        logger.info("Initializing fallback SQLite database.")
        
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'database',
            'schema.sql'
        )
        
        if not os.path.exists(schema_path):
            logger.error(f"Schema SQL file not found at {schema_path}")
            return
            
        conn = get_sqlite_connection()
        try:
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            conn.executescript(schema_sql)
            conn.commit()
            logger.info("SQLite schema initialized successfully.")
            
            # Seed an admin user if none exists
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Admins")
            if cursor.fetchone()[0] == 0:
                from werkzeug.security import generate_password_hash
                hashed_pwd = generate_password_hash("admin123")
                cursor.execute(
                    "INSERT INTO Admins (admin_id, name, email, password) VALUES (?, ?, ?, ?)",
                    ("admin_default", "System Administrator", "admin@sims.com", hashed_pwd)
                )
                conn.commit()
                logger.info("Default Admin account seeded: admin@sims.com / admin123")
                
        except Exception as e:
            logger.error(f"Error initializing SQLite database: {e}")
        finally:
            conn.close()
        return

    # Otherwise, Snowflake is the primary database
    DB_ENGINE = 'snowflake'
    logger.info("Using Snowflake as primary database. Verifying connection...")
    try:
        conn = get_snowflake_connection()
        conn.close()
        logger.info("Snowflake connection verified successfully.")
    except Exception as e:
        logger.error(f"Snowflake connection verification failed during startup: {e}")
        raise e
def is_snowflake():
    """Returns True if the active database engine is Snowflake, initializing it if needed."""
    global DB_ENGINE
    if DB_ENGINE is None:
        init_db()
    return DB_ENGINE == 'snowflake'

def get_db_connection():
    """Returns the active database connection."""
    global DB_ENGINE
    
    if DB_ENGINE is None:
        init_db()
        
    if DB_ENGINE == 'snowflake':
        return get_snowflake_connection()
        
    return get_sqlite_connection()

def process_snowflake_row(row):
    """Processes Snowflake rows to format resume details, skills, and bios dynamically."""
    if not row:
        return row
        
    # Parse skills and bio
    if 'skills' in row:
        val = row['skills'] or ''
        if " ||| " in val:
            skills, bio = val.split(" ||| ", 1)
            row['skills'] = skills
            row['bio'] = bio
        else:
            row['skills'] = val
            row['bio'] = row.get('bio') or ''
            
    if 'student_skills' in row:
        val = row['student_skills'] or ''
        if " ||| " in val:
            skills, bio = val.split(" ||| ", 1)
            row['student_skills'] = skills
            row['student_bio'] = bio
        else:
            row['student_skills'] = val
            row['student_bio'] = row.get('student_bio') or ''
            
    # Format resume path and name
    if 'resume_name' in row or 'resume_path' in row:
        resume = row.get('resume_name') or row.get('resume_path') or ''
        if resume:
            row['resume_name'] = resume
            if not resume.startswith('static/'):
                row['resume_path'] = f"static/uploads/resumes/{resume}"
            else:
                row['resume_path'] = resume
        else:
            row['resume_name'] = ''
            row['resume_path'] = ''
            
    return row

def execute_query(query, params=None, fetch=None):
    """
    Executes a parameterized query on the active database engine.
    Automatically handles parameter placeholders.
    """
    conn = get_db_connection()
    global DB_ENGINE
    
    try:
        cursor = conn.cursor()
        
        # Transform placeholders/tables based on DB engine
        if DB_ENGINE == 'sqlite':
            query = query.replace('%s', '?')
            
        sql_params = params if params is not None else ()
        cursor.execute(query, sql_params)
        
        if fetch == 'all':
            rows = cursor.fetchall()
            if DB_ENGINE == 'snowflake':
                # Convert Snowflake row tuples to dict list using column names
                columns = [col[0].lower() for col in cursor.description]
                return [process_snowflake_row(dict(zip(columns, row))) for row in rows]
            else:
                # SQLite dict conversion
                return [dict(row) for row in rows]
                
        elif fetch == 'one':
            row = cursor.fetchone()
            if row is None:
                return None
            if DB_ENGINE == 'snowflake':
                columns = [col[0].lower() for col in cursor.description]
                return process_snowflake_row(dict(zip(columns, row)))
            else:
                return dict(row)
                
        else:
            conn.commit()
            if DB_ENGINE == 'sqlite':
                return cursor.lastrowid
            return cursor.rowcount
            
    except Exception as e:
        logger.error(f"Database execution error under {DB_ENGINE} engine: {e}")
        try:
            conn.rollback()
        except:
            pass
        raise e
    finally:
        try:
            conn.close()
        except:
            pass
