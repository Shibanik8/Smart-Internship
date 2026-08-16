from flask import Blueprint
from controllers.student_controller import StudentController

student_bp = Blueprint('student', __name__, url_prefix='/student')

student_bp.route('/dashboard')(StudentController.dashboard)
student_bp.route('/profile')(StudentController.profile)
student_bp.route('/profile/edit', methods=['GET', 'POST'])(StudentController.edit_profile)
student_bp.route('/internships')(StudentController.list_internships)
student_bp.route('/internships/<internship_id>')(StudentController.internship_details)
student_bp.route('/internships/<internship_id>/apply', methods=['POST'])(StudentController.apply_internship)
student_bp.route('/applications')(StudentController.my_applications)
