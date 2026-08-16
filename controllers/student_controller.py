import os
from flask import render_template, redirect, url_for, flash, request, session, current_app
from werkzeug.utils import secure_filename
from models.student import Student
from models.internship import Internship
from models.application import Application
from services.skill_analysis import SkillAnalysisService
from services.recommendation import RecommendationEngine
from services.verification import DocumentVerificationService

# Allowed extensions for resumes
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class StudentController:
    @staticmethod
    def dashboard():
        if session.get('role') != 'student':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        student_id = session.get('user_id')
        student = Student.get_by_id(student_id)
        applications = Application.get_by_student(student_id)
        
        # Recommendations
        all_internships = Internship.get_all()
        recommendations = RecommendationEngine.get_recommendations(student.get('skills', ''), all_internships)
        
        # Document Verification status (UiPath integration placeholder)
        verifications = DocumentVerificationService.get_verification_status(student_id)
        
        return render_template(
            'student/dashboard.html', 
            student=student, 
            applications=applications,
            recommendations=recommendations,
            verifications=verifications
        )

    @staticmethod
    def profile():
        if session.get('role') != 'student':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        student_id = session.get('user_id')
        student = Student.get_by_id(student_id)
        return render_template('student/profile.html', student=student)

    @staticmethod
    def edit_profile():
        if session.get('role') != 'student':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        student_id = session.get('user_id')
        student = Student.get_by_id(student_id)
        
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            bio = request.form.get('bio', '').strip()
            skills = request.form.get('skills', '').strip()
            
            # Handle File Upload
            resume_file = request.files.get('resume')
            resume_name = student.get('resume_name')
            resume_path = student.get('resume_path')
            
            if resume_file and resume_file.filename != '':
                if allowed_file(resume_file.filename):
                    filename = secure_filename(f"{student_id}_{resume_file.filename}")
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'resumes')
                    
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder, exist_ok=True)
                        
                    filepath = os.path.join(upload_folder, filename)
                    resume_file.save(filepath)
                    
                    resume_name = resume_file.filename
                    resume_path = f"static/uploads/resumes/{filename}"
                    
                    # Trigger UiPath Verification Placeholder
                    DocumentVerificationService.trigger_verification(student_id, resume_name)
                    flash("Resume uploaded. UiPath scanning started automatically.", "info")
                else:
                    flash("Invalid file format. Please upload PDF, DOC, or DOCX.", "warning")
            
            try:
                Student.update_profile(student_id, name, bio, skills, resume_name, resume_path)
                flash("Profile updated successfully.", "success")
                return redirect(url_for('student.profile'))
            except Exception as e:
                flash(f"Error updating profile: {e}", "danger")
                
        return render_template('student/edit_profile.html', student=student)

    @staticmethod
    def list_internships():
        if session.get('role') != 'student':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        search_query = request.args.get('search', '').strip()
        internships = Internship.search(search_query)
        return render_template('student/internships.html', internships=internships, search_query=search_query)

    @staticmethod
    def internship_details(internship_id):
        if session.get('role') != 'student':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        student_id = session.get('user_id')
        internship = Internship.get_by_id(internship_id)
        if not internship:
            flash("Internship not found.", "danger")
            return redirect(url_for('student.list_internships'))
            
        student = Student.get_by_id(student_id)
        already_applied = Application.has_applied(student_id, internship_id)
        
        # Skill Gap Analysis Integration
        skill_analysis = SkillAnalysisService.analyze_skills(
            student.get('skills', ''), 
            internship.get('skills_required', '')
        )
        
        return render_template(
            'student/internship_details.html', 
            internship=internship, 
            already_applied=already_applied,
            analysis=skill_analysis
        )

    @staticmethod
    def apply_internship(internship_id):
        if session.get('role') != 'student':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        student_id = session.get('user_id')
        
        # Enforce that student has a resume uploaded before applying
        student = Student.get_by_id(student_id)
        if not student.get('resume_path'):
            flash("Please upload a resume in your profile before applying.", "warning")
            return redirect(url_for('student.edit_profile'))
            
        success = Application.apply(internship_id, student_id)
        if success:
            flash("Application submitted successfully!", "success")
        else:
            flash("You have already applied to this internship.", "warning")
            
        return redirect(url_for('student.my_applications'))

    @staticmethod
    def my_applications():
        if session.get('role') != 'student':
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))
            
        student_id = session.get('user_id')
        applications = Application.get_by_student(student_id)
        return render_template('student/applications.html', applications=applications)
