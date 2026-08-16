import uuid
from datetime import datetime
from database.connection import execute_query, is_snowflake

def clean_stipend(stipend):
    if not stipend:
        return 0
    # Extract only digits from stipend string
    digits = ''.join(c for c in str(stipend) if c.isdigit())
    return int(digits) if digits else 0

class Internship:
    @staticmethod
    def create(company_id, title, description, location, requirements, skills_required, duration, stipend):
        """Creates a new internship listing."""
        internship_id = f"int_{uuid.uuid4().hex[:10]}"
        
        if is_snowflake():
            stipend_val = clean_stipend(stipend)
            execute_query(
                "INSERT INTO INTERNSHIP_DB.PUBLIC.INTERNSHIP (INTERNSHIPID, COMPANYID, JOBTITLE, REQUIREDSKILLS, DURATION, STIPEND, LOCATION, LASTDATE) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (internship_id, company_id, title, skills_required, duration, stipend_val, location, datetime.now())
            )
        else:
            execute_query(
                "INSERT INTO Internships (internship_id, company_id, title, description, location, requirements, skills_required, duration, stipend, created_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (internship_id, company_id, title, description, location, requirements, skills_required, duration, stipend, datetime.now())
            )
        return internship_id

    @staticmethod
    def update(internship_id, title, description, location, requirements, skills_required, duration, stipend):
        """Updates an existing internship listing."""
        if is_snowflake():
            stipend_val = clean_stipend(stipend)
            execute_query(
                "UPDATE INTERNSHIP_DB.PUBLIC.INTERNSHIP SET JOBTITLE = %s, REQUIREDSKILLS = %s, DURATION = %s, STIPEND = %s, LOCATION = %s WHERE INTERNSHIPID = %s",
                (title, skills_required, duration, stipend_val, location, internship_id)
            )
        else:
            execute_query(
                "UPDATE Internships SET title = %s, description = %s, location = %s, requirements = %s, "
                "skills_required = %s, duration = %s, stipend = %s WHERE internship_id = %s",
                (title, description, location, requirements, skills_required, duration, stipend, internship_id)
            )

    @staticmethod
    def delete(internship_id):
        """Deletes an internship and its active applications."""
        if is_snowflake():
            execute_query("DELETE FROM APPLICATIONS WHERE INTERNSHIPID = %s", (internship_id,))
            execute_query("DELETE FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP WHERE INTERNSHIPID = %s", (internship_id,))
        else:
            execute_query("DELETE FROM Applications WHERE internship_id = %s", (internship_id,))
            execute_query("DELETE FROM Internships WHERE internship_id = %s", (internship_id,))

    @staticmethod
    def get_by_id(internship_id):
        """Retrieves details of an internship including the company details."""
        if is_snowflake():
            return execute_query(
                "SELECT i.INTERNSHIPID as internship_id, i.COMPANYID as company_id, i.JOBTITLE as title, '' as description, i.LOCATION as location, "
                "'' as requirements, i.REQUIREDSKILLS as skills_required, i.DURATION as duration, CAST(i.STIPEND as VARCHAR) as stipend, i.LASTDATE as created_at, "
                "c.C2 as company_name, c.C6 as company_website, '' as company_description "
                "FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP i "
                "JOIN COMPANIES c ON i.COMPANYID = c.C1 "
                "WHERE i.INTERNSHIPID = %s",
                (internship_id,),
                fetch='one'
            )
        else:
            return execute_query(
                "SELECT i.*, c.name as company_name, c.website as company_website, c.description as company_description "
                "FROM Internships i "
                "JOIN Companies c ON i.company_id = c.company_id "
                "WHERE i.internship_id = %s",
                (internship_id,),
                fetch='one'
            )

    @staticmethod
    def get_by_company(company_id):
        """Retrieves all internships posted by a specific company."""
        if is_snowflake():
            return execute_query(
                "SELECT INTERNSHIPID as internship_id, COMPANYID as company_id, JOBTITLE as title, '' as description, LOCATION as location, "
                "'' as requirements, REQUIREDSKILLS as skills_required, DURATION as duration, CAST(STIPEND as VARCHAR) as stipend, LASTDATE as created_at "
                "FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP WHERE COMPANYID = %s ORDER BY LASTDATE DESC",
                (company_id,),
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT * FROM Internships WHERE company_id = %s ORDER BY created_at DESC",
                (company_id,),
                fetch='all'
            )

    @staticmethod
    def get_all():
        """Retrieves all internships with company name."""
        if is_snowflake():
            return execute_query(
                "SELECT i.INTERNSHIPID as internship_id, i.COMPANYID as company_id, i.JOBTITLE as title, '' as description, i.LOCATION as location, "
                "'' as requirements, i.REQUIREDSKILLS as skills_required, i.DURATION as duration, CAST(i.STIPEND as VARCHAR) as stipend, i.LASTDATE as created_at, "
                "c.C2 as company_name "
                "FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP i "
                "JOIN COMPANIES c ON i.COMPANYID = c.C1 "
                "ORDER BY i.LASTDATE DESC",
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT i.*, c.name as company_name "
                "FROM Internships i "
                "JOIN Companies c ON i.company_id = c.company_id "
                "ORDER BY i.created_at DESC",
                fetch='all'
            )

    @staticmethod
    def search(query_text):
        """Searches internships by title, location, skills required, or company name."""
        if not query_text:
            return Internship.get_all()
            
        if is_snowflake():
            term = f"%{query_text}%"
            return execute_query(
                "SELECT i.INTERNSHIPID as internship_id, i.COMPANYID as company_id, i.JOBTITLE as title, '' as description, i.LOCATION as location, "
                "'' as requirements, i.REQUIREDSKILLS as skills_required, i.DURATION as duration, CAST(i.STIPEND as VARCHAR) as stipend, i.LASTDATE as created_at, "
                "c.C2 as company_name "
                "FROM INTERNSHIP_DB.PUBLIC.INTERNSHIP i "
                "JOIN COMPANIES c ON i.COMPANYID = c.C1 "
                "WHERE i.JOBTITLE LIKE %s OR i.LOCATION LIKE %s OR i.REQUIREDSKILLS LIKE %s OR c.C2 LIKE %s "
                "ORDER BY i.LASTDATE DESC",
                (term, term, term, term),
                fetch='all'
            )
        else:
            term = f"%{query_text}%"
            return execute_query(
                "SELECT i.*, c.name as company_name "
                "FROM Internships i "
                "JOIN Companies c ON i.company_id = c.company_id "
                "WHERE i.title LIKE %s OR i.description LIKE %s OR i.location LIKE %s OR i.skills_required LIKE %s OR c.name LIKE %s "
                "ORDER BY i.created_at DESC",
                (term, term, term, term, term),
                fetch='all'
            )
