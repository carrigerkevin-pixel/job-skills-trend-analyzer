"""Keyword-based skill extraction from job description text.

Uses regex word-boundary matching against the skill variants defined
in skills_list.py to identify which technical skills are mentioned
in a given piece of text.
"""

import re
from skills_list import SKILLS


def extract_skills_from_text(text):
    """Find all known skills mentioned in a piece of text.

    Args:
        text (str): The job description text to search. Can be None
            or empty, in which case an empty list is returned.

    Returns:
        list[str]: Display names of skills found (e.g. ["Python", "AWS"]),
            in no particular order. Each skill appears at most once,
            even if multiple variants match.
    """
    
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