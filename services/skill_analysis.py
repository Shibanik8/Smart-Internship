class SkillAnalysisService:
    @staticmethod
    def analyze_skills(student_skills_str, target_skills_str):
        """
        Compares a student's skills against an internship's required skills.
        Returns a dictionary with match percentage, matching skills, missing skills, and course recommendations.
        """
        if not student_skills_str:
            student_skills = []
        else:
            student_skills = [s.strip().lower() for s in student_skills_str.split(',') if s.strip()]
            
        if not target_skills_str:
            target_skills = []
        else:
            target_skills = [s.strip().lower() for s in target_skills_str.split(',') if s.strip()]
            
        if not target_skills:
            return {
                "match_percentage": 100,
                "matching_skills": student_skills,
                "missing_skills": [],
                "recommendations": []
            }
            
        matching = [s for s in student_skills if s in target_skills]
        missing = [s for s in target_skills if s not in student_skills]
        
        match_percentage = int((len(matching) / len(target_skills)) * 100)
        
        # Course library mapped to skills
        course_db = {
            "python": ["Complete Python BootCamp (Udemy)", "Python for Data Science (Coursera)"],
            "sql": ["SQL for Analytics (DataCamp)", "Mastering SQL Queries (edX)"],
            "snowflake": ["Snowflake Essentials (Pluralsight)", "Snowflake SnowPro Core Preparation"],
            "bootstrap": ["Responsive Web Design with Bootstrap 5 (Udemy)", "Bootstrap 5 Beginner to Advanced"],
            "javascript": ["JavaScript: The Weird Parts (Udemy)", "Modern JavaScript from the Beginning"],
            "flask": ["Flask Web Development (O'Reilly)", "REST APIs with Flask and Python"],
            "uipath": ["UiPath RPA Developer Foundation", "Automation in Enterprise with UiPath"],
            "power bi": ["Power BI Masterclass (Udemy)", "Analyzing Data with Power BI (Microsoft)"]
        }
        
        recommendations = []
        for skill in missing:
            courses = course_db.get(skill, [f"Introduction to {skill.capitalize()} (Coursera)", f"Advanced {skill.capitalize()} Tutorial"])
            recommendations.append({
                "skill": skill.capitalize(),
                "courses": courses
            })
            
        return {
            "match_percentage": match_percentage,
            "matching_skills": [s.capitalize() for s in matching],
            "missing_skills": [s.capitalize() for s in missing],
            "recommendations": recommendations
        }
