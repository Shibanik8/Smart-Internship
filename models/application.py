import uuid
from datetime import datetime
from database.connection import execute_query, is_snowflake

class Application:
    @staticmethod
    def apply(internship_id, student_id):
        """Creates a new internship application."""
        # Prevent duplicates
        if Application.has_applied(student_id, internship_id):
            return None
            
        application_id = f"app_{uuid.uuid4().hex[:10]}"
        
        if is_snowflake():
            execute_query(
                "INSERT INTO APPLICATIONS (APPLICATIONID, INTERNSHIPID, STUDENTID, STATUS, APPLICATIONDATE) "
                "VALUES (%s, %s, %s, %s, %s)",
                (application_id, internship_id, student_id, 'Applied', datetime.now())
            )
        else:
            execute_query(
                "INSERT INTO Applications (application_id, internship_id, student_id, status, applied_at) "
                "VALUES (%s, %s, %s, %s, %s)",
                (application_id, internship_id, student_id, 'Applied', datetime.now())
            )
        return application_id

    @staticmethod
    def has_applied(student_id, internship_id):
        """Checks if a student has already applied to an internship."""
        if is_snowflake():
            res = execute_query(
                "SELECT COUNT(*) as cnt FROM APPLICATIONS WHERE STUDENTID = %s AND INTERNSHIPID = %s",
                (student_id, internship_id),
                fetch='one'
            )
            return res['cnt'] > 0
        else:
            res = execute_query(
                "SELECT COUNT(*) as cnt FROM Applications WHERE student_id = %s AND internship_id = %s",
                (student_id, internship_id),
                fetch='one'
            )
            return res['cnt'] > 0

    @staticmethod
    def update_status(application_id, status):
        """Updates the application status (e.g. Reviewed, Accepted, Rejected)."""
        if is_snowflake():
            execute_query(
                "UPDATE APPLICATIONS SET STATUS = %s WHERE APPLICATIONID = %s",
                (status, application_id)
            )
        else:
            execute_query(
                "UPDATE Applications SET status = %s WHERE application_id = %s",
                (status, application_id)
            )

    @staticmethod
    def get_by_student(student_id):
        """Retrieves all applications submitted by a student, with internship and company details."""
        if is_snowflake():
            return execute_query(
                "SELECT a.APPLICATIONID as application_id, a.INTERNSHIPID as internship_id, a.STUDENTID as student_id, a.STATUS as status, a.APPLICATIONDATE as applied_at, "
                "i.JOBTITLE as internship_title, i.LOCATION as internship_location, c.C2 as company_name "
                "FROM APPLICATIONS a "
                "JOIN INTERNSHIP_DB.PUBLIC.INTERNSHIP i ON a.INTERNSHIPID = i.INTERNSHIPID "
                "JOIN COMPANIES c ON i.COMPANYID = c.C1 "
                "WHERE a.STUDENTID = %s "
                "ORDER BY a.APPLICATIONDATE DESC",
                (student_id,),
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT a.*, i.title as internship_title, i.location as internship_location, c.name as company_name "
                "FROM Applications a "
                "JOIN Internships i ON a.internship_id = i.internship_id "
                "JOIN Companies c ON i.company_id = c.company_id "
                "WHERE a.student_id = %s "
                "ORDER BY a.applied_at DESC",
                (student_id,),
                fetch='all'
            )

    @staticmethod
    def get_by_company(company_id):
        """Retrieves all applications for internships posted by a specific company."""
        if is_snowflake():
            return execute_query(
                "SELECT a.APPLICATIONID as application_id, a.INTERNSHIPID as internship_id, a.STUDENTID as student_id, a.STATUS as status, a.APPLICATIONDATE as applied_at, "
                "i.JOBTITLE as internship_title, s.FULLNAME as student_name, s.EMAIL as student_email "
                "FROM APPLICATIONS a "
                "JOIN INTERNSHIP_DB.PUBLIC.INTERNSHIP i ON a.INTERNSHIPID = i.INTERNSHIPID "
                "JOIN STUDENTS s ON a.STUDENTID = s.STUDENTID "
                "WHERE i.COMPANYID = %s "
                "ORDER BY a.APPLICATIONDATE DESC",
                (company_id,),
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT a.*, i.title as internship_title, s.name as student_name, s.email as student_email "
                "FROM Applications a "
                "JOIN Internships i ON a.internship_id = i.internship_id "
                "JOIN Students s ON a.student_id = s.student_id "
                "WHERE i.company_id = %s "
                "ORDER BY a.applied_at DESC",
                (company_id,),
                fetch='all'
            )

    @staticmethod
    def get_by_id(application_id):
        """Retrieves details of a specific application."""
        if is_snowflake():
            return execute_query(
                "SELECT a.APPLICATIONID as application_id, a.INTERNSHIPID as internship_id, a.STUDENTID as student_id, a.STATUS as status, a.APPLICATIONDATE as applied_at, "
                "i.JOBTITLE as internship_title, i.REQUIREDSKILLS as internship_skills, s.FULLNAME as student_name, s.EMAIL as student_email, "
                "'' as student_bio, s.SKILLS as student_skills, s.RESUME as student_resume_name, s.RESUME as student_resume_path, "
                "c.C2 as company_name, c.C1 as company_id "
                "FROM APPLICATIONS a "
                "JOIN INTERNSHIP_DB.PUBLIC.INTERNSHIP i ON a.INTERNSHIPID = i.INTERNSHIPID "
                "JOIN STUDENTS s ON a.STUDENTID = s.STUDENTID "
                "JOIN COMPANIES c ON i.COMPANYID = c.C1 "
                "WHERE a.APPLICATIONID = %s",
                (application_id,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT a.*, i.title as internship_title, i.skills_required as internship_skills, s.name as student_name, s.email as student_email, "
                "s.bio as student_bio, s.skills as student_skills, s.resume_name as student_resume_name, s.resume_path as student_resume_path, "
                "c.name as company_name, c.company_id "
                "FROM Applications a "
                "JOIN Internships i ON a.internship_id = i.internship_id "
                "JOIN Students s ON a.student_id = s.student_id "
                "JOIN Companies c ON i.company_id = c.company_id "
                "WHERE a.application_id = %s",
                (application_id,),
                fetch='one'
            )

    @staticmethod
    def get_all():
        """Retrieves all applications across the entire system."""
        if is_snowflake():
            return execute_query(
                "SELECT a.APPLICATIONID as application_id, a.INTERNSHIPID as internship_id, a.STUDENTID as student_id, a.STATUS as status, a.APPLICATIONDATE as applied_at, "
                "i.JOBTITLE as internship_title, s.FULLNAME as student_name, c.C2 as company_name "
                "FROM APPLICATIONS a "
                "JOIN INTERNSHIP_DB.PUBLIC.INTERNSHIP i ON a.INTERNSHIPID = i.INTERNSHIPID "
                "JOIN STUDENTS s ON a.STUDENTID = s.STUDENTID "
                "JOIN COMPANIES c ON i.COMPANYID = c.C1 "
                "ORDER BY a.APPLICATIONDATE DESC",
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT a.*, i.title as internship_title, s.name as student_name, c.name as company_name "
                "FROM Applications a "
                "JOIN Internships i ON a.internship_id = i.internship_id "
                "JOIN Students s ON a.student_id = s.student_id "
                "JOIN Companies c ON i.company_id = c.company_id "
                "ORDER BY a.applied_at DESC",
                fetch='all'
            )

    @staticmethod
    def delete(application_id):
        """Deletes an application."""
        if is_snowflake():
            execute_query("DELETE FROM APPLICATIONS WHERE APPLICATIONID = %s", (application_id,))
        else:
            execute_query("DELETE FROM Applications WHERE application_id = %s", (application_id,))
