from flask import render_template, redirect, url_for, flash, request, session
from models.admin import Admin
from models.student import Student
from models.company import Company
from models.internship import Internship
from models.application import Application
from services.powerbi import PowerBiService

class AdminController:
    @staticmethod
    def dashboard():
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        stats = Admin.get_system_stats()
        
        # Load sample recent records for the dashboard feed
        recent_students = Student.get_all()[:5]
        recent_companies = Company.get_all()[:5]
        recent_internships = Internship.get_all()[:5]
        recent_applications = Application.get_all()[:5]
        
        return render_template(
            'admin/dashboard.html',
            stats=stats,
            students=recent_students,
            companies=recent_companies,
            internships=recent_internships,
            applications=recent_applications
        )

    @staticmethod
    def manage_students():
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        students = Student.get_all()
        return render_template('admin/students.html', students=students)

    @staticmethod
    def delete_student(student_id):
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        try:
            Student.delete(student_id)
            flash("Student profile and matching applications deleted.", "success")
        except Exception as e:
            flash(f"Error deleting student: {e}", "danger")
        return redirect(url_for('admin.manage_students'))

    @staticmethod
    def manage_companies():
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        companies = Company.get_all()
        return render_template('admin/companies.html', companies=companies)

    @staticmethod
    def delete_company(company_id):
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        try:
            Company.delete(company_id)
            flash("Company, their job listings, and applicants deleted successfully.", "success")
        except Exception as e:
            flash(f"Error deleting company: {e}", "danger")
        return redirect(url_for('admin.manage_companies'))

    @staticmethod
    def manage_internships():
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        internships = Internship.get_all()
        return render_template('admin/internships.html', internships=internships)

    @staticmethod
    def delete_internship(internship_id):
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        try:
            Internship.delete(internship_id)
            flash("Internship listing and active application links deleted.", "success")
        except Exception as e:
            flash(f"Error deleting internship: {e}", "danger")
        return redirect(url_for('admin.manage_internships'))

    @staticmethod
    def manage_applications():
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        applications = Application.get_all()
        return render_template('admin/applications.html', applications=applications)

    @staticmethod
    def delete_application(application_id):
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        try:
            Application.delete(application_id)
            flash("Application record purged from system logs.", "success")
        except Exception as e:
            flash(f"Error deleting application: {e}", "danger")
        return redirect(url_for('admin.manage_applications'))

    @staticmethod
    def view_statistics():
        if session.get('role') != 'admin':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        stats = Admin.get_system_stats()
        powerbi_config = PowerBiService.get_dashboard_config()
        
        return render_template(
            'admin/statistics.html',
            stats=stats,
            powerbi=powerbi_config
        )
