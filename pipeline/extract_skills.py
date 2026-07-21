import re
from skills_list import SKILLS


def extract_skills_from_text(text):
    """Given a job description, return a list of skill display names found in it."""
    if not text:
        return []

    text_lower = text.lower()
    found_skills = []

    for display_name, variants in SKILLS.items():
        for variant in variants:
            # \b = word boundary, so "js" won't match inside "objects"
            pattern = r"\b" + re.escape(variant) + r"\b"
            if re.search(pattern, text_lower):
                found_skills.append(display_name)
                break  # no need to check other variants once we've found a match

    return found_skills


if __name__ == "__main__":
    # Quick manual test
    sample = "We are looking for a Python developer with experience in AWS, Docker, and REST APIs. Familiarity with React.js is a plus."
    result = extract_skills_from_text(sample)
    print("Skills found:", result)