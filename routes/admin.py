from flask import Blueprint
from controllers.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

admin_bp.route('/dashboard')(AdminController.dashboard)
admin_bp.route('/students')(AdminController.manage_students)
admin_bp.route('/students/delete/<student_id>', methods=['POST'])(AdminController.delete_student)
admin_bp.route('/companies')(AdminController.manage_companies)
admin_bp.route('/companies/delete/<company_id>', methods=['POST'])(AdminController.delete_company)
admin_bp.route('/internships')(AdminController.manage_internships)
admin_bp.route('/internships/delete/<internship_id>', methods=['POST'])(AdminController.delete_internship)
admin_bp.route('/applications')(AdminController.manage_applications)
admin_bp.route('/applications/delete/<application_id>', methods=['POST'])(AdminController.delete_application)
admin_bp.route('/statistics')(AdminController.view_statistics)
