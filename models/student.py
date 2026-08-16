import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import execute_query, is_snowflake

class Student:
    @staticmethod
    def create(name, email, password):
        """Creates a new student account with a hashed password."""
        student_id = f"std_{uuid.uuid4().hex[:10]}"
        hashed_password = generate_password_hash(password)
        
        if is_snowflake():
            execute_query(
                "INSERT INTO STUDENTS (STUDENTID, FULLNAME, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s)",
                (student_id, name, email, hashed_password)
            )
        else:
            execute_query(
                "INSERT INTO Students (student_id, name, email, password, created_at) VALUES (%s, %s, %s, %s, %s)",
                (student_id, name, email, hashed_password, datetime.now())
            )
        return student_id

    @staticmethod
    def get_by_email(email):
        """Retrieves a student by email address."""
        if is_snowflake():
            return execute_query(
                "SELECT STUDENTID as student_id, FULLNAME as name, EMAIL as email, PASSWORD as password, SKILLS as skills, RESUME as resume_name, RESUME as resume_path, '' as bio, NULL as created_at FROM STUDENTS WHERE EMAIL = %s",
                (email,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT * FROM Students WHERE email = %s",
                (email,),
                fetch='one'
            )

    @staticmethod
    def get_by_id(student_id):
        """Retrieves a student by student ID."""
        if is_snowflake():
            return execute_query(
                "SELECT STUDENTID as student_id, FULLNAME as name, EMAIL as email, PASSWORD as password, SKILLS as skills, RESUME as resume_name, RESUME as resume_path, '' as bio, NULL as created_at FROM STUDENTS WHERE STUDENTID = %s",
                (student_id,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT * FROM Students WHERE student_id = %s",
                (student_id,),
                fetch='one'
            )

    @staticmethod
    def update_profile(student_id, name, bio, skills, resume_name=None, resume_path=None):
        """Updates the student profile fields."""
        if is_snowflake():
            serialized_skills = f"{skills or ''} ||| {bio or ''}"
            if resume_name is not None:
                execute_query(
                    "UPDATE STUDENTS SET FULLNAME = %s, SKILLS = %s, RESUME = %s WHERE STUDENTID = %s",
                    (name, serialized_skills, resume_name, student_id)
                )
            else:
                execute_query(
                    "UPDATE STUDENTS SET FULLNAME = %s, SKILLS = %s WHERE STUDENTID = %s",
                    (name, serialized_skills, student_id)
                )
        else:
            if resume_name is not None and resume_path is not None:
                execute_query(
                    "UPDATE Students SET name = %s, bio = %s, skills = %s, resume_name = %s, resume_path = %s WHERE student_id = %s",
                    (name, bio, skills, resume_name, resume_path, student_id)
                )
            else:
                execute_query(
                    "UPDATE Students SET name = %s, bio = %s, skills = %s WHERE student_id = %s",
                    (name, bio, skills, student_id)
                )

    @staticmethod
    def get_all():
        """Retrieves all students."""
        if is_snowflake():
            return execute_query(
                "SELECT STUDENTID as student_id, FULLNAME as name, EMAIL as email, PASSWORD as password, SKILLS as skills, RESUME as resume_name, RESUME as resume_path, '' as bio, NULL as created_at FROM STUDENTS ORDER BY STUDENTID DESC",
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT * FROM Students ORDER BY created_at DESC",
                fetch='all'
            )

    @staticmethod
    def delete(student_id):
        """Deletes a student account and their applications."""
        if is_snowflake():
            execute_query("DELETE FROM APPLICATIONS WHERE STUDENTID = %s", (student_id,))
            execute_query("DELETE FROM DOCUMENT_VERIFICATION WHERE STUDENTID = %s", (student_id,))
            execute_query("DELETE FROM STUDENTS WHERE STUDENTID = %s", (student_id,))
        else:
            execute_query("DELETE FROM Applications WHERE student_id = %s", (student_id,))
            execute_query("DELETE FROM DocumentVerification WHERE student_id = %s", (student_id,))
            execute_query("DELETE FROM Students WHERE student_id = %s", (student_id,))

    @staticmethod
    def verify_password(hashed_password, password):
        """Checks if password matches hashed password."""
        try:
            if check_password_hash(hashed_password, password):
                return True
        except Exception:
            pass
        return hashed_password == password
