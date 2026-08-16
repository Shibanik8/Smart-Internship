from flask import render_template, redirect, url_for, flash, request, session
from models.student import Student
from models.company import Company
from models.admin import Admin

class AuthController:
    @staticmethod
    def student_register():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            if not name or not email or not password:
                flash("All fields are required.", "danger")
                return render_template('auth/student_register.html')
                
            if Student.get_by_email(email) or Company.get_by_email(email) or Admin.get_by_email(email):
                flash("Email already registered in the system.", "danger")
                return render_template('auth/student_register.html')
                
            try:
                Student.create(name, email, password)
                flash("Registration successful. Please log in.", "success")
                return redirect(url_for('auth.student_login'))
            except Exception as e:
                flash(f"Error during registration: {e}", "danger")
                
        return render_template('auth/student_register.html')

    @staticmethod
    def student_login():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            if not email or not password:
                flash("All fields are required.", "danger")
                return render_template('auth/student_login.html')
                
            student = Student.get_by_email(email)
            if student and Student.verify_password(student['password'], password):
                session.clear()
                session['user_id'] = student['student_id']
                session['name'] = student['name']
                session['email'] = student['email']
                session['role'] = 'student'
                flash(f"Welcome back, {student['name']}!", "success")
                return redirect(url_for('student.dashboard'))
            else:
                flash("Invalid email or password.", "danger")
                
        return render_template('auth/student_login.html')

    @staticmethod
    def company_register():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            if not name or not email or not password:
                flash("All fields are required.", "danger")
                return render_template('auth/company_register.html')
                
            if Student.get_by_email(email) or Company.get_by_email(email) or Admin.get_by_email(email):
                flash("Email already registered in the system.", "danger")
                return render_template('auth/company_register.html')
                
            try:
                Company.create(name, email, password)
                flash("Registration successful. Please log in.", "success")
                return redirect(url_for('auth.company_login'))
            except Exception as e:
                flash(f"Error during registration: {e}", "danger")
                
        return render_template('auth/company_register.html')

    @staticmethod
    def company_login():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            if not email or not password:
                flash("All fields are required.", "danger")
                return render_template('auth/company_login.html')
                
            company = Company.get_by_email(email)
            if company and Company.verify_password(company['password'], password):
                session.clear()
                session['user_id'] = company['company_id']
                session['name'] = company['name']
                session['email'] = company['email']
                session['role'] = 'company'
                flash(f"Welcome, {company['name']} team!", "success")
                return redirect(url_for('company.dashboard'))
            else:
                flash("Invalid email or password.", "danger")
                
        return render_template('auth/company_login.html')

    @staticmethod
    def admin_login():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            if not email or not password:
                flash("All fields are required.", "danger")
                return render_template('auth/admin_login.html')
                
            admin = Admin.get_by_email(email)
            if admin and Admin.verify_password(admin['password'], password):
                session.clear()
                session['user_id'] = admin['admin_id']
                session['name'] = admin['name']
                session['email'] = admin['email']
                session['role'] = 'admin'
                flash(f"Logged in successfully as Administrator.", "success")
                return redirect(url_for('admin.dashboard'))
            else:
                flash("Invalid admin credentials.", "danger")
                
        return render_template('auth/admin_login.html')

    @staticmethod
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for('home'))
