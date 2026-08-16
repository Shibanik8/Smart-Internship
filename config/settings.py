import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_internship_management_system_super_secret_key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    
    # Snowflake Connection Parameters
    SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT', '')
    SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER', '')
    SNOWFLAKE_PASSWORD = os.environ.get('SNOWFLAKE_PASSWORD', '')
    SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE', '')
    SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE', '')
    SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA', '')
    SNOWFLAKE_ROLE = os.environ.get('SNOWFLAKE_ROLE', '')
    
    # Explicit SQLite fallback config for local testing
    USE_SQLITE = os.environ.get('USE_SQLITE', 'False').lower() == 'true'
    
    # SQLite Fallback DB Path
    SQLITE_DB_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        'database', 
        'database.db'
    )
