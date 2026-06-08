# Resume Anonymization - removes PII to reduce bias during scoring
import re

def anonymize_resume(text, candidate_name=None):
    """
    Anonymize resume by removing PII.

    Args:
        text: Raw resume text

    Returns:
        str: Anonymized text
    """
    # Remove emails
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)

    # Remove phone numbers
    text = re.sub(r'\d{3}[-.]?\d{3}[-.]?\d{4}', '[PHONE]', text)

    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '[URL]', text)

    # Remove the candidate's name (each part, whole-word, case-insensitive)
    if candidate_name:
        for part in candidate_name.split():
            if len(part) > 1:  # skip single initials
                text = re.sub(rf'\b{re.escape(part)}\b', '[NAME]', text, flags=re.IGNORECASE)

    return text
