import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pipeline"))

import streamlit as st
from analysis import top_skills_overall

st.set_page_config(page_title="Job Skills Trend Analyzer", layout="wide")

st.title("📊 Job Skills Trend Analyzer")
st.write("Discover which skills are most in-demand across tech job postings.")

st.header("Top Skills Overall")

skills_data = top_skills_overall(limit=10)

for item in skills_data:
    st.write(f"**{item['skill']}**: {item['count']} mentions")