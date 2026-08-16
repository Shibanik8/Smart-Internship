from database.connection import execute_query, is_snowflake
from werkzeug.security import check_password_hash

class Admin:
    @staticmethod
    def get_by_email(email):
        """Retrieves an admin by email address."""
        if is_snowflake():
            return execute_query(
                "SELECT ADMINID as admin_id, FULLNAME as name, EMAIL as email, PASSWORD as password FROM ADMIN WHERE EMAIL = %s",
                (email,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT * FROM Admins WHERE email = %s",
                (email,),
                fetch='one'
            )

    @staticmethod
    def get_by_id(admin_id):
        """Retrieves an admin by ID."""
        if is_snowflake():
            return execute_query(
                "SELECT ADMINID as admin_id, FULLNAME as name, EMAIL as email, PASSWORD as password FROM ADMIN WHERE ADMINID = %s",
                (admin_id,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT * FROM Admins WHERE admin_id = %s",
                (admin_id,),
                fetch='one'
            )

    @staticmethod
    def verify_password(hashed_password, password):
        """Checks if password matches hashed password."""
        try:
            if check_password_hash(hashed_password, password):
                return True
        except Exception:
            pass
        return hashed_password == password

    @staticmethod
    def get_system_stats():
        """Calculates system metrics: counts of students, companies, internships, applications, etc."""
        if is_snowflake():
            students_count = execute_query("SELECT COUNT(*) as cnt FROM STUDENTS", fetch='one')['cnt']
            # Exclude header row if present in COMPANIES (CompanyName check or similar)
            companies_count = execute_query("SELECT COUNT(*) as cnt FROM COMPANIES WHERE C1 <> 'CompanyID'", fetch='one')['cnt']
            internships_count = execute_query("SELECT COUNT(*) as cnt FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP", fetch='one')['cnt']
            applications_count = execute_query("SELECT COUNT(*) as cnt FROM APPLICATIONS", fetch='one')['cnt']
            
            # Get application status distribution
            status_rows = execute_query(
                "SELECT STATUS as status, COUNT(*) as cnt FROM APPLICATIONS GROUP BY STATUS",
                fetch='all'
            )
            status_dist = {row['status']: row['cnt'] for row in status_rows}
        else:
            students_count = execute_query("SELECT COUNT(*) as cnt FROM Students", fetch='one')['cnt']
            companies_count = execute_query("SELECT COUNT(*) as cnt FROM Companies", fetch='one')['cnt']
            internships_count = execute_query("SELECT COUNT(*) as cnt FROM Internships", fetch='one')['cnt']
            applications_count = execute_query("SELECT COUNT(*) as cnt FROM Applications", fetch='one')['cnt']
            
            # Get application status distribution
            status_rows = execute_query(
                "SELECT status, COUNT(*) as cnt FROM Applications GROUP BY status",
                fetch='all'
            )
            status_dist = {row['status']: row['cnt'] for row in status_rows}
        
        return {
            "students": students_count,
            "companies": companies_count,
            "internships": internships_count,
            "applications": applications_count,
            "status_distribution": status_dist
        }
