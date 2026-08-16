from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/student/register', methods=['GET', 'POST'])(AuthController.student_register)
auth_bp.route('/student/login', methods=['GET', 'POST'])(AuthController.student_login)
auth_bp.route('/company/register', methods=['GET', 'POST'])(AuthController.company_register)
auth_bp.route('/company/login', methods=['GET', 'POST'])(AuthController.company_login)
auth_bp.route('/admin/login', methods=['GET', 'POST'])(AuthController.admin_login)
auth_bp.route('/logout')(AuthController.logout)
