class RecommendationEngine:
    @staticmethod
    def get_recommendations(student_skills_str, all_internships):
        """
        Filters and scores internships based on student skills.
        Returns a sorted list of internships with a matching score.
        """
        if not student_skills_str:
            return [{"internship": i, "score": 50, "reason": "Complete your profile to see tailored recommendations."} for i in all_internships[:3]]
            
        student_skills = [s.strip().lower() for s in student_skills_str.split(',') if s.strip()]
        recommendations = []
        
        for internship in all_internships:
            target_skills_str = internship.get('skills_required', '')
            if not target_skills_str:
                continue
                
            target_skills = [s.strip().lower() for s in target_skills_str.split(',') if s.strip()]
            matching = [s for s in student_skills if s in target_skills]
            
            if not target_skills:
                score = 50
            else:
                score = int((len(matching) / len(target_skills)) * 100)
            
            # Formulate a reason
            if score >= 70:
                reason = "Highly matches your skills in: " + ", ".join([s.capitalize() for s in matching[:3]])
            elif score >= 30:
                reason = "Matches some of your skills in: " + ", ".join([s.capitalize() for s in matching[:3]])
            else:
                reason = "Opportunity to learn: " + ", ".join([s.capitalize() for s in target_skills[:3]])
                
            recommendations.append({
                "internship": internship,
                "score": score,
                "reason": reason
            })
            
        # Sort recommendations by score descending
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:5]
