"""Interactive dashboard for exploring job skill trend data.

A Streamlit app that lets users filter skill trends by job category
and adjust how many top skills to display, visualized as a sorted
bar chart. Reads data via the analysis functions in analysis.py.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pipeline"))

import streamlit as st
import pandas as pd
from analysis import top_skills_overall, top_skills_by_category, all_categories
import altair as alt

st.set_page_config(page_title="Job Skills Trend Analyzer", layout="wide")

st.title("📊 Job Skills Trend Analyzer")
st.write("Discover which skills are most in-demand across tech job postings.")

# --- Sidebar controls ---
st.sidebar.header("Filters")

categories = all_categories()
category_options = ["All categories"] + sorted(categories)

selected_category = st.sidebar.selectbox("Job category", category_options)

limit = st.sidebar.slider("Number of skills to show", min_value=5, max_value=20, value=10)

# --- Main content ---
if selected_category == "All categories":
    st.header("Top Skills Overall")
    skills_data = top_skills_overall(limit=limit)
else:
    st.header(f"Top Skills for: {selected_category.title()}")
    skills_data = top_skills_by_category(selected_category, limit=limit)

if skills_data:
    df = pd.DataFrame(skills_data)
    df = df.sort_values("count", ascending=False)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("skill", sort="-y", title="Skill"),
            y=alt.Y("count", title="Mentions"),
            tooltip=["skill", "count"]
        )
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.write("No skill data found for this category yet.")