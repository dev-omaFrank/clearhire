def generate_explanation(match_score, skills_match, experience_score, tfidf_score=None):
    """
    Generate AI recommendation explanation.

    Args:
        match_score: Overall match percentage
        skills_match: Dict with matched, missing, extra skills
        experience_score: Experience score percentage
        tfidf_score: TF-IDF similarity score (optional)

    Returns:
        str: Human-readable explanation
    """
    explanations = []
    
    # Match level
    if match_score >= 70:
        explanations.append("• Strong Match based on skills")
    elif match_score >= 50:
        explanations.append("• Moderate Match based on skills")
    else:
        explanations.append("• Weak Match based on skills")
        
    # Experience level
    if experience_score >= 80:
        explanations.append(f"• Candidate has very valid experience (Excellent)")
    elif experience_score >= 60:
        explanations.append(f"• Candidate possess good experience (Moderate)")
    elif experience_score >= 40:
        explanations.append(f"• Candidate has some experience in this field (Fair)")
    else:
        explanations.append(f"• Candidate has limited experience in this field (Poor)")

    # Matched skills
    if skills_match['matched']:
        explanations.append(f"<br>Candidate possesses the following skills: {'<br>•'.join(skills_match['matched'][:3])}")

    # Missing skills
    if skills_match['missing']:
        explanations.append(f"<br>Candidate lacks the following skills: {'<br>•'.join(skills_match['missing'][:3])}")

    return "<br>".join(explanations)

def get_status(match_score):
    """Get employment status based on score."""
    if match_score >= 70:
        return "Employable"
    elif match_score >= 50:
        return "Fair"
    else:
        return "Not employable"

def classify_submission(score, threshold):
    """Single source of truth for status label + badge type (threshold-relative).

    Employable:     score >= 70
    Fair:           threshold <= score < 70
    Not employable: score < threshold
    """
    score = score or 0
    threshold = int(threshold) if threshold else 0
    if score >= 70:
        return "Employable", "success"
    elif score >= threshold:
        return "Fair", "warning"
    else:
        return "Not employable", "danger"

def combine_scores(tfidf_score, skills_match_percentage, experience_score):
    """Combine all scores into final percentage."""
    final_score = (
        tfidf_score * 0.30 +           
        skills_match_percentage * 0.30 + 
        experience_score * 0.40          
    )
    return round(final_score, 2)