from flask import Blueprint
from controllers.company_controller import CompanyController

company_bp = Blueprint('company', __name__, url_prefix='/company')

company_bp.route('/dashboard')(CompanyController.dashboard)
company_bp.route('/profile')(CompanyController.profile)
company_bp.route('/profile/edit', methods=['GET', 'POST'])(CompanyController.edit_profile)
company_bp.route('/internship/post', methods=['GET', 'POST'])(CompanyController.post_internship)
company_bp.route('/internship/edit/<internship_id>', methods=['GET', 'POST'])(CompanyController.edit_internship)
company_bp.route('/internship/delete/<internship_id>', methods=['POST'])(CompanyController.delete_internship)
company_bp.route('/internships')(CompanyController.list_internships)
company_bp.route('/applicants')(CompanyController.list_applicants)
company_bp.route('/applicants/<application_id>')(CompanyController.applicant_details)
company_bp.route('/applicants/<application_id>/accept', methods=['POST'])(CompanyController.accept_applicant)
company_bp.route('/applicants/<application_id>/reject', methods=['POST'])(CompanyController.reject_applicant)
