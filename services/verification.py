import uuid
from datetime import datetime
from database.connection import execute_query, is_snowflake

class DocumentVerificationService:
    @staticmethod
    def trigger_verification(student_id, document_name):
        """
        Simulates triggering a UiPath Robot to verify a document (e.g. Resume).
        Creates a DocumentVerification record as 'Pending' and then updates it to 'Verified'.
        """
        verification_id = f"ver_{uuid.uuid4().hex[:10]}"
        
        if is_snowflake():
            # Insert a pending verification record in Snowflake
            execute_query(
                "INSERT INTO DOCUMENT_VERIFICATION (VERIFICATIONID, STUDENTID, DOCUMENTNAME, VERIFICATIONSTATUS, VERIFIEDDATE) VALUES (%s, %s, %s, %s, %s)",
                (verification_id, student_id, document_name, 'Pending', datetime.now())
            )
            
            # Simulate quick UiPath automation verification (immediately mark it as Verified in mock environment)
            execute_query(
                "UPDATE DOCUMENT_VERIFICATION SET VERIFICATIONSTATUS = %s, VERIFIEDDATE = %s WHERE VERIFICATIONID = %s",
                ('Verified', datetime.now(), verification_id)
            )
        else:
            # Insert a pending verification record in SQLite
            execute_query(
                "INSERT INTO DocumentVerification (verification_id, student_id, document_name, status, verified_at) VALUES (%s, %s, %s, %s, %s)",
                (verification_id, student_id, document_name, 'Pending', datetime.now())
            )
            
            # Simulate quick UiPath automation verification (immediately mark it as Verified in mock environment)
            execute_query(
                "UPDATE DocumentVerification SET status = %s, verified_at = %s WHERE verification_id = %s",
                ('Verified', datetime.now(), verification_id)
            )
        
        return {
            "verification_id": verification_id,
            "status": "Verified",
            "message": f"UiPath Robot successfully scanned and verified {document_name}."
        }

    @staticmethod
    def get_verification_status(student_id):
        """Retrieves document verification records for a student."""
        if is_snowflake():
            return execute_query(
                "SELECT VERIFICATIONID as verification_id, STUDENTID as student_id, DOCUMENTNAME as document_name, VERIFICATIONSTATUS as status, VERIFIEDDATE as verified_at "
                "FROM DOCUMENT_VERIFICATION WHERE STUDENTID = %s ORDER BY VERIFIEDDATE DESC",
                (student_id,),
                fetch='all'
            )
        else:
            return execute_query(
                "SELECT * FROM DocumentVerification WHERE student_id = %s ORDER BY verified_at DESC",
                (student_id,),
                fetch='all'
            )
