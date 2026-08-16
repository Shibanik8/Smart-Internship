from flask import render_template, redirect, url_for, flash, request, session
from models.company import Company
from models.internship import Internship
from models.application import Application
from services.skill_analysis import SkillAnalysisService

class CompanyController:
    @staticmethod
    def dashboard():
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        company_id = session.get('user_id')
        company = Company.get_by_id(company_id)
        internships = Internship.get_by_company(company_id)
        applicants = Application.get_by_company(company_id)
        
        # Calculate summary metrics
        total_postings = len(internships)
        total_applicants = len(applicants)
        pending_applicants = len([a for a in applicants if a['status'] == 'Applied'])
        
        return render_template(
            'company/dashboard.html',
            company=company,
            internships=internships[:5],
            applicants=applicants[:5],
            total_postings=total_postings,
            total_applicants=total_applicants,
            pending_applicants=pending_applicants
        )

    @staticmethod
    def profile():
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        company_id = session.get('user_id')
        company = Company.get_by_id(company_id)
        return render_template('company/profile.html', company=company)

    @staticmethod
    def edit_profile():
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        company_id = session.get('user_id')
        company = Company.get_by_id(company_id)
        
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            website = request.form.get('website', '').strip()
            location = request.form.get('location', '').strip()
            description = request.form.get('description', '').strip()
            
            if not name:
                flash("Company Name is required.", "warning")
                return render_template('company/edit_profile.html', company=company)
                
            try:
                Company.update_profile(company_id, name, website, location, description)
                flash("Profile updated successfully.", "success")
                return redirect(url_for('company.profile'))
            except Exception as e:
                flash(f"Error updating profile: {e}", "danger")
                
        return render_template('company/edit_profile.html', company=company)

    @staticmethod
    def post_internship():
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        if request.method == 'POST':
            company_id = session.get('user_id')
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            location = request.form.get('location', '').strip()
            requirements = request.form.get('requirements', '').strip()
            skills_required = request.form.get('skills_required', '').strip()
            duration = request.form.get('duration', '').strip()
            stipend = request.form.get('stipend', '').strip()
            
            if not title or not description or not location:
                flash("Title, Description, and Location are required.", "warning")
                return render_template('company/post_internship.html')
                
            try:
                Internship.create(company_id, title, description, location, requirements, skills_required, duration, stipend)
                flash("Internship posted successfully!", "success")
                return redirect(url_for('company.list_internships'))
            except Exception as e:
                flash(f"Error posting internship: {e}", "danger")
                
        return render_template('company/post_internship.html')

    @staticmethod
    def edit_internship(internship_id):
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        internship = Internship.get_by_id(internship_id)
        if not internship or internship['company_id'] != session.get('user_id'):
            flash("Internship not found or unauthorized.", "danger")
            return redirect(url_for('company.list_internships'))
            
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            location = request.form.get('location', '').strip()
            requirements = request.form.get('requirements', '').strip()
            skills_required = request.form.get('skills_required', '').strip()
            duration = request.form.get('duration', '').strip()
            stipend = request.form.get('stipend', '').strip()
            
            if not title or not description or not location:
                flash("Title, Description, and Location are required.", "warning")
                return render_template('company/edit_internship.html', internship=internship)
                
            try:
                Internship.update(internship_id, title, description, location, requirements, skills_required, duration, stipend)
                flash("Internship updated successfully!", "success")
                return redirect(url_for('company.list_internships'))
            except Exception as e:
                flash(f"Error updating internship: {e}", "danger")
                
        return render_template('company/edit_internship.html', internship=internship)

    @staticmethod
    def delete_internship(internship_id):
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        internship = Internship.get_by_id(internship_id)
        if not internship or internship['company_id'] != session.get('user_id'):
            flash("Internship not found or unauthorized.", "danger")
            return redirect(url_for('company.list_internships'))
            
        try:
            Internship.delete(internship_id)
            flash("Internship deleted successfully.", "success")
        except Exception as e:
            flash(f"Error deleting internship: {e}", "danger")
            
        return redirect(url_for('company.list_internships'))

    @staticmethod
    def list_internships():
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        company_id = session.get('user_id')
        internships = Internship.get_by_company(company_id)
        return render_template('company/internships.html', internships=internships)

    @staticmethod
    def list_applicants():
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        company_id = session.get('user_id')
        applicants = Application.get_by_company(company_id)
        return render_template('company/applicants.html', applicants=applicants)

    @staticmethod
    def applicant_details(application_id):
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        application = Application.get_by_id(application_id)
        if not application or application['company_id'] != session.get('user_id'):
            flash("Application record not found or unauthorized.", "danger")
            return redirect(url_for('company.list_applicants'))
            
        # Optional: update status to 'Reviewed' if it was 'Applied'
        if application['status'] == 'Applied':
            Application.update_status(application_id, 'Reviewed')
            application['status'] = 'Reviewed'
            
        # Run Skill Gap Analysis on student skills against internship required skills
        skill_analysis = SkillAnalysisService.analyze_skills(
            application.get('student_skills', ''),
            application.get('internship_skills', '')
        )
        
        return render_template(
            'company/applicant_details.html',
            application=application,
            analysis=skill_analysis
        )

    @staticmethod
    def accept_applicant(application_id):
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        application = Application.get_by_id(application_id)
        if not application or application['company_id'] != session.get('user_id'):
            flash("Application record not found or unauthorized.", "danger")
            return redirect(url_for('company.list_applicants'))
            
        try:
            Application.update_status(application_id, 'Accepted')
            flash("Application accepted successfully.", "success")
        except Exception as e:
            flash(f"Error accepting application: {e}", "danger")
            
        return redirect(url_for('company.applicant_details', application_id=application_id))

    @staticmethod
    def reject_applicant(application_id):
        if session.get('role') != 'company':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        application = Application.get_by_id(application_id)
        if not application or application['company_id'] != session.get('user_id'):
            flash("Application record not found or unauthorized.", "danger")
            return redirect(url_for('company.list_applicants'))
            
        try:
            Application.update_status(application_id, 'Rejected')
            flash("Application rejected.", "info")
        except Exception as e:
            flash(f"Error rejecting application: {e}", "danger")
            
        return redirect(url_for('company.applicant_details', application_id=application_id))
