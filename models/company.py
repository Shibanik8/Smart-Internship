import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import execute_query, is_snowflake

class Company:
    @staticmethod
    def create(name, email, password):
        """Creates a new company account with a hashed password."""
        company_id = f"com_{uuid.uuid4().hex[:10]}"
        hashed_password = generate_password_hash(password)
        
        if is_snowflake():
            execute_query(
                "INSERT INTO COMPANIES (C1, C2, C3, C7) VALUES (%s, %s, %s, %s)",
                (company_id, name, email, hashed_password)
            )
        else:
            execute_query(
                "INSERT INTO Companies (company_id, name, email, password, created_at) VALUES (%s, %s, %s, %s, %s)",
                (company_id, name, email, hashed_password, datetime.now())
            )
        return company_id

    @staticmethod
    def get_by_email(email):
        """Retrieves a company by email address."""
        if is_snowflake():
            return execute_query(
                "SELECT C1 as company_id, C2 as name, C3 as email, C7 as password, C5 as location, C6 as website, '' as description, NULL as created_at FROM COMPANIES WHERE C3 = %s",
                (email,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT * FROM Companies WHERE email = %s",
                (email,),
                fetch='one'
            )

    @staticmethod
    def get_by_id(company_id):
        """Retrieves a company by company ID."""
        if is_snowflake():
            return execute_query(
                "SELECT C1 as company_id, C2 as name, C3 as email, C7 as password, C5 as location, C6 as website, '' as description, NULL as created_at FROM COMPANIES WHERE C1 = %s",
                (company_id,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT * FROM Companies WHERE company_id = %s",
                (company_id,),
                fetch='one'
            )

    @staticmethod
    def update_profile(company_id, name, website, location, description):
        """Updates company profile info."""
        if is_snowflake():
            execute_query(
                "UPDATE COMPANIES SET C2 = %s, C6 = %s, C5 = %s WHERE C1 = %s",
                (name, website, location, company_id)
            )
        else:
            execute_query(
                "UPDATE Companies SET name = %s, website = %s, location = %s, description = %s WHERE company_id = %s",
                (name, website, location, description, company_id)
            )

    @staticmethod
    def get_all():
        """Retrieves all companies."""
        if is_snowflake():
            return execute_query(
                "SELECT C1 as company_id, C2 as name, C3 as email, C7 as password, C5 as location, C6 as website, '' as description, NULL as created_at FROM COMPANIES ORDER BY C1 DESC",
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT * FROM Companies ORDER BY created_at DESC",
                fetch='all'
            )

    @staticmethod
    def delete(company_id):
        """Deletes a company account and all related internships and applications."""
        if is_snowflake():
            # Get internship IDs for company
            internships = execute_query(
                "SELECT INTERNSHIPID as internship_id FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP WHERE COMPANYID = %s",
                (company_id,),
                fetch='all'
            )
            for i in internships:
                execute_query("DELETE FROM APPLICATIONS WHERE INTERNSHIPID = %s", (i['internship_id'],))
                
            execute_query("DELETE FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP WHERE COMPANYID = %s", (company_id,))
            execute_query("DELETE FROM COMPANIES WHERE C1 = %s", (company_id,))
        else:
            # Get internship IDs for company
            internships = execute_query(
                "SELECT internship_id FROM Internships WHERE company_id = %s",
                (company_id,),
                fetch='all'
            )
            for i in internships:
                execute_query("DELETE FROM Applications WHERE internship_id = %s", (i['internship_id'],))
                
            execute_query("DELETE FROM Internships WHERE company_id = %s", (company_id,))
            execute_query("DELETE FROM Companies WHERE company_id = %s", (company_id,))

    @staticmethod
    def verify_password(hashed_password, password):
        """Checks if password matches hashed password."""
        try:
            if check_password_hash(hashed_password, password):
                return True
        except Exception:
            pass
        return hashed_password == password
