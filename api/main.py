import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pipeline"))

from fastapi import FastAPI, HTTPException
from analysis import top_skills_overall, top_skills_by_category, all_categories

app = FastAPI(title="Job Skills Trend Analyzer API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Skills Trend Analyzer API"}


@app.get("/skills/top")
def get_top_skills(limit: int = 10):
    """Get the most frequently mentioned skills across all job postings."""
    return top_skills_overall(limit=limit)


@app.get("/categories")
def get_categories():
    """Get the list of job categories being tracked."""
    return all_categories()


@app.get("/skills/by-category/{category}")
def get_skills_by_category(category: str, limit: int = 10):
    """Get the top skills for a specific job category."""
    valid_categories = all_categories()
    if category not in valid_categories:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found. Valid categories: {valid_categories}"
        )
    return top_skills_by_category(category, limit=limit)