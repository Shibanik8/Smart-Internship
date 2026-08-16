from flask import Flask, render_template, session
from config.settings import Config
from database.connection import init_db
from routes.auth import auth_bp
from routes.student import student_bp
from routes.company import company_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database tables and seed administrator account
with app.app_context():
    init_db()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    """Home / Landing page route."""
    return render_template('index.html')

# Global context processor to share active user info or roles
@app.context_processor
def inject_user_details():
    return {
        'logged_in_user_role': session.get('role'),
        'logged_in_user_name': session.get('name')
    }

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )