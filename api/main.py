"""FastAPI backend serving job skill trend data.

Exposes REST endpoints that wrap the analysis functions in
analysis.py, allowing the Streamlit dashboard (or any other client)
to fetch skill trend data over HTTP.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pipeline"))

from fastapi import FastAPI, HTTPException
from analysis import top_skills_overall, top_skills_by_category, all_categories

app = FastAPI(title="Job Skills Trend Analyzer API")


@app.get("/")
def read_root():
    """Health check / welcome endpoint."""
    return {"message": "Welcome to the Job Skills Trend Analyzer API"}


@app.get("/skills/top")
def get_top_skills(limit: int = 10):
    """Get the most frequently mentioned skills across all job postings.

    Args:
        limit (int): Maximum number of skills to return (query parameter).
    """
    return top_skills_overall(limit=limit)


@app.get("/categories")
def get_categories():
    """Get the list of job categories being tracked."""
    return all_categories()


@app.get("/skills/by-category/{category}")
def get_skills_by_category(category: str, limit: int = 10):
    """Get the top skills for a specific job category.

    Args:
        category (str): The job category to filter by (path parameter),
            e.g. "backend developer".
        limit (int): Maximum number of skills to return (query parameter).

    Raises:
        HTTPException: 404 if the category doesn't exist in the data.
    """
    valid_categories = all_categories()
    if category not in valid_categories:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found. Valid categories: {valid_categories}"
        )
    return top_skills_by_category(category, limit=limit)